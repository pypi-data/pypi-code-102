from abc import ABCMeta, abstractmethod
from typing import Dict, MutableMapping, Optional, Sequence, \
    Tuple

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.sql.elements import Label

__all__ = [
    'AbstractGroupByViewMixin',
]


class AbstractGroupByViewMixin(metaclass=ABCMeta):
    """
    Abstract view for grouping
    """
    @abstractmethod
    def _get_params_getall(self, param: str) -> Sequence[str]: ...

    def _get_group_by_params(self, model_fields: Sequence[str]) -> Optional[
        Tuple[str, ...]
    ]:
        """
        Получение параметров group_by.

        :param model_fields: Список доступных полей основной модели.
        :return:
        """
        group_by_params = self._get_params_getall('group_by')
        if not group_by_params:
            return

        group_by_params = tuple(
            filter(
                lambda x: x in model_fields,
                group_by_params,
            ),
        )

        if not group_by_params:
            return

        return group_by_params

    def _handle_group_by_params(
        self,
        db_cls: DeclarativeMeta,
        db_joins: MutableMapping[str, str],
    ) -> Tuple[
        Tuple[str, ...],
        Optional[Tuple[Label, ...]],
        Optional[Dict[str, Tuple[str, DeclarativeMeta]]],
    ]:

        mapper = inspect(db_cls)

        group_by_params = self._get_group_by_params(list(mapper.columns.keys()))
        if not group_by_params:
            return group_by_params, None, None

        relationships = mapper.relationships
        relationships_map = {
            # fixme: получать ключ более гибко
            f'{k}_id': k for k, r in relationships.items()
        }

        # при группировке невозможна стыковка никаких моделей, кроме тех,
        # поля которых участвуют в группировке
        db_joins_keys = list(db_joins.keys())
        allowed_relationships = [
            v for k, v in relationships_map.items()
            if k in group_by_params
        ]
        for key in db_joins_keys:
            if key not in allowed_relationships:
                del db_joins[key]

        return group_by_params, tuple(
            getattr(db_cls, c).label(c) for c in group_by_params
        ), {
            k: (v, relationships[v].mapper.class_)
            for k, v in relationships_map.items()
            if k in group_by_params
        }
