import logging
import threading
import time
from threading import Thread
from typing import Optional, Iterable

from eventy.messaging.agent import Agent, Handler, Guarantee
from eventy.messaging.service import Service
from eventy.messaging.store import Cursor, RecordStore, RecordWriteStore
from eventy.record import Record, Response, RecordType
from eventy.trace_id.local import local_trace

__all__ = [
    'EventyApp',
]

logger = logging.getLogger(__name__)


class EventyApp:
    """
    EventyApp is the messaging application.
    """

    def __init__(
        self,
        record_store: RecordStore,
        app_service: Service,
        ext_services: Iterable[Service] = None,
        agents: Iterable[Agent] = None,
        handlers: Iterable[Handler] = None,
        read_batch_size: int = 1,
        read_timeout_ms: Optional[int] = None,
        write_timeout_ms: Optional[int] = None,
        ack_timeout_ms: Optional[int] = None,
        commit_timeout_ms: Optional[int] = None,
    ):
        self._record_store = record_store
        self._app_service = app_service
        self._ext_services = ext_services or []
        self._all_handlers = list()
        if handlers is not None:
            for handler in handlers:
                self._all_handlers.append(handler)
        if agents is not None:
            for agent in agents:
                for handler in agent.handlers:
                    self._all_handlers.append(handler)

        self._read_batch_size = read_batch_size
        self._read_timeout_ms = read_timeout_ms
        self._write_timeout_ms = write_timeout_ms
        self._ack_timeout_ms = ack_timeout_ms
        self._commit_timeout_ms = commit_timeout_ms

        self._write_store = _AppRecordWriteStore(self)
        self.started = False
        self.cancelled = False

    def _get_service_for_name(self, service_name: Optional[str]):
        if service_name is None:
            return self._app_service
        for service in self._ext_services:
            if service.name == service_name:
                return service
        raise ValueError(f"Service {service_name} not found.")

    def _get_topics_to_register(self) -> list[str]:
        topics: set[str] = set()
        topics.add(self._app_service.request_topic)
        for handler in self._all_handlers:
            logger.debug(f"Found handler {handler}.")
            service = self._get_service_for_name(handler.service_name)
            topics.add(service.topic_for(handler.record_type))
        return list(sorted(topics))

    def _get_handlers_for_record(self, record: Record, guarantee: Guarantee) -> list[Handler]:
        handlers: list[Handler] = list()
        for handler in self._all_handlers:
            if (
                handler.record_type == record.type
                and handler.record_name == record.name
                and handler.delivery_guarantee == guarantee
                and self._get_service_for_name(handler.service_name).namespace == record.namespace
            ):
                if isinstance(record, Response):
                    if record.destination == self._app_service.namespace:
                        handlers.append(handler)
                else:
                    handlers.append(handler)
        return handlers

    def _get_topic_for_record(self, record: Record) -> str:
        if record.type == RecordType.EVENT or record.type == RecordType.RESPONSE:
            return self._app_service.topic_for(record.type)
        for service in self._ext_services:
            if service.namespace == record.namespace:
                return service.topic_for(record.type)
        raise ValueError(f"No topic for record {record}.")

    @property
    def write_store(self) -> RecordWriteStore:
        return self._write_store

    def _process_one_batch(self) -> None:
        records = list(
            self._record_store.read(
                max_count=self._read_batch_size,
                timeout_ms=self._read_timeout_ms,
                auto_ack=False,
            )
        )
        if records:
            logger.debug(f"Received {len(records)} new records.")
        else:
            time.sleep(0.1)
            return

        # At Least Once
        for record in records:
            with local_trace(correlation_id=record.correlation_id):
                try:
                    for handler in self._get_handlers_for_record(record, Guarantee.AT_LEAST_ONCE):
                        for output_record in handler.handle_record(record):
                            self._record_store.write(
                                output_record,
                                self._get_topic_for_record(output_record),
                                self._write_timeout_ms,
                            )
                except Exception as e:
                    logger.error(f"Failed to process record {record}: {e}")

        # Exactly Once
        self._record_store.start_transaction()
        self._record_store.ack(self._ack_timeout_ms)
        for record in records:
            with local_trace(correlation_id=record.correlation_id):
                for handler in self._get_handlers_for_record(record, Guarantee.EXACTLY_ONCE):
                    for output_record in handler.handle_record(record):
                        self._record_store.write(
                            output_record,
                            self._get_topic_for_record(output_record),
                            self._write_timeout_ms,
                        )
        self._record_store.commit(self._commit_timeout_ms)

        # At Most Once
        for record in records:
            with local_trace(correlation_id=record.correlation_id):
                for handler in self._get_handlers_for_record(record, Guarantee.AT_MOST_ONCE):
                    for output_record in handler.handle_record(record):
                        self._record_store.write(
                            output_record,
                            self._get_topic_for_record(output_record),
                            self._write_timeout_ms,
                        )

    def run(self, keep_alive=False) -> None:
        """
        Run in a separate thread.

        :param keep_alive: If True, the app will not exit until the calling thread is finished.
        """
        logger.info(f"Starting Eventy App.")

        topics_to_register = self._get_topics_to_register()
        logger.info(
            f"Starting Eventy App: registering {len(topics_to_register)} topics: {', '.join(topics_to_register)}."
        )
        for topic in topics_to_register:
            logger.debug(f"Will register to topic: {topic}.")
            try:
                self._record_store.register_topic(topic, Cursor.ACKNOWLEDGED)
            except Exception as e:
                logger.error(f"Failed to register to topic {topic}: {e}")

        current_thread = threading.current_thread()

        def run_loop():
            while True:
                if self.cancelled:
                    finish_reason = "cancelled"
                    break
                elif not keep_alive and not current_thread.is_alive():
                    finish_reason = "parent thread not alive"
                    break
                else:
                    try:
                        self._process_one_batch()
                    except Exception as e:
                        logger.error("Failed to process batch.", e)
                        finish_reason = "failed to process batch"
                        break
            logger.warning(f"Stopped processing records. Reason: {finish_reason}.")

        self.process_thread = Thread(target=run_loop)

        logger.info(f"Starting Eventy App: starting processing thread.")
        self.process_thread.start()
        self.started = True

        logger.info(f"Starting Eventy App: started.")

    def __del__(self):
        logger.info(f"Stopping Eventy App.")
        if self.started:
            logger.info(f"Waiting process thread to join.")
            self.cancelled = True
            self.process_thread.join()
            logger.info(f"Process thread joined.")


class _AppRecordWriteStore(RecordWriteStore):
    def __init__(self, app: EventyApp):
        self._app = app

    def write(self, record: Record) -> None:
        with local_trace(correlation_id=record.correlation_id):
            self._app._record_store.write(
                record,
                self._app._get_topic_for_record(record),
                self._app._write_timeout_ms,
            )
