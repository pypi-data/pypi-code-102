# from modules.torch_sdk_code.events.span_event import SpanAbortedEvent, SpanEndEvent, SpanStartEvent
from torch_sdk.models.span import Span, SpanEventType, SpanStatus
from torch_sdk.events.span_event import SpanEvent
from enum import Enum
import logging

logger = logging.getLogger('torch_sdk_code')
logger.setLevel(logging.INFO)


class SpanContextStatus(Enum):
    INITIALISED = 1
    STARTED = 2
    ABORTED = 3
    FINISHED = 4
    FAILED = 5

class SpanContext:

    def __init__(self, client=None, span: Span = None, parent=None, context_data= None, new_span: bool = None):
        """
        Description:
            SpanContext is used for instantiate event for given span.
        :param client: TorchClient class instance
        :param span: Span class instance
        :param parent: SpanContext class instance which parent of current span context
        :param new_span: pass true value when its new span
        """
        self.client = client
        self.span = span
        self.parent = parent
        # self.status = SpanContextStatus.INITIALISED
        self.status = span.status
        self.started = True
        if new_span is None:
            new_span = False
        self.new_span = new_span
        # if self.status == SpanContextStatus.STARTED.name:
        #     self.started = True
        # else:
        if new_span or self.status == SpanContextStatus.INITIALISED.name:
            self.start(context_data=context_data)
        self.children = []

    def __repr__(self):
        return f"SpanContext({self.__dict__})"

    def is_span_finished(self):
        if self.span.status == SpanStatus.ABORTED.name or self.span.status == SpanStatus.FINISHED.name:
            logger.info('Can not send any event. Span is already completed')
            return True
        else:
            return False

    def start(self, context_data: dict = None):
        """
        Description:
            used to start span event
        :param context_data: context data of the span
        :return: SpanContextEvent class instance of the started span event
        """
        if self.is_span_finished():
            return
        if not self.started and self.status == SpanContextStatus.STARTED.name:
            logger.info('Can not start span that is already started')
            return
        span_event = SpanEvent()
        event_res = span_event.convert(
            event_uid=SpanEventType.SPAN_START.value,
            client=self.client,
            context_data=context_data,
            span_id=self.span.id
        )
        self.started = True
        self.started = SpanContextStatus.STARTED
        return event_res

    def end(self, context_data: dict = None):
        """
        Description:
            used to end span event
        :param context_data: context data of the span
        :return: SpanContextEvent class instance of the ended span event
        """
        if self.is_span_finished():
            return None
        if not self.started:
            logger.info('Can not end span that is not started.')
            return
        if self.status == SpanContextStatus.FINISHED:
            logger.info('Can not end span that is finished already.')
            return
        self.started = True
        span_event = SpanEvent()
        event_res = span_event.convert(
            event_uid=SpanEventType.SPAN_END.value,
            client=self.client,
            context_data=context_data,
            span_id=self.span.id
        )
        self.status = SpanContextStatus.FINISHED
        return event_res

    def abort(self, context_data: dict = None):
        """
        Description:
            used to abort span event
        :param context_data: context data of the span
        :return: SpanContextEvent class instance of the aborted span event
        """
        if self.is_span_finished():
            return
        if not self.started:
            logger.info('Can not abort span that is not started yet')
            return
        if self.status == SpanContextStatus.ABORTED:
            logger.info('Can not abort span that is aborted already.')
            return
        span_event = SpanEvent()
        event_res = span_event.convert(
            event_uid=SpanEventType.SPAN_ABORTED.value,
            client=self.client,
            context_data=context_data,
            span_id=self.span.id
        )
        self.status = SpanContextStatus.ABORTED
        return event_res

    def failed(self, context_data: dict = None):
        """
        Description:
            used to fail span event
        :param context_data: context data of the span
        :return: SpanContextEvent class instance of the failed span event
        """
        if self.is_span_finished():
            return
        if not self.started:
            logger.info('Can not fail span that is not started yet')
            return
        if self.status == SpanContextStatus.FAILED:
            logger.info('Can not fail span that is aborted failed.')
            return
        span_event = SpanEvent()
        event_res = span_event.convert(
            event_uid=SpanEventType.SPAN_FAILED.value,
            client=self.client,
            context_data=context_data,
            span_id=self.span.id
        )
        self.status = SpanContextStatus.FAILED
        return event_res

    def send_event(self, span_event):
        if self.is_span_finished():
            return
        if not self.started:
            logger.info('Can not send custom event for given span context because span is not started yet. Kindly '
                        'start it '
                        'first.')
            return

        log_data = None
        if span_event.event_uid == 'LOG':
            log_data = span_event.log_data
        return span_event.convert(
            event_uid=span_event.event_uid,
            client=self.client,
            context_data=span_event.context_data,
            span_id=self.span.id,
            log_data=log_data
        )

    def create_child_span(self, uid: str, context_data: dict = None, associatedJobUids = None):
        """
            Used to create child span context of the current span context
        :param context_data: context to start span
        :param uid: uid of the new span you want to create
        :return: spanContext class instance for the newly created span
        """
        if uid is None:
            Exception('To create a child span uid is required.')

        create_child_span = Span(
            uid=uid,
            pipelineRunId=self.span.pipelineRunId,
            parentSpanId=self.span.id
        )
        payload = create_child_span.__dict__
        payload['status'] = create_child_span.status.name
        if associatedJobUids is None:
            associatedJobUids = []
        child_span_payload = {'span': payload, 'associatedJobUids' : associatedJobUids}
        res = self.client.create_span(self.span.pipelineRunId, child_span_payload)
        span_context = SpanContext(client=self.client, span=res, parent=self, context_data= context_data, new_span= True)
        self.children.append(span_context)
        return span_context

    def has_children(self):
        """
        Description:
            To check whether given spanContext has children or not.
        :return: True if it has children else False
        """
        return len(self.children) > 0

    def is_root(self):
        """
        Description:
            To check whether given spanContext is root or not.
        :return: True if it is root else False
        """
        return self.parent is None
