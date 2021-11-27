import itertools
from abc import ABCMeta, abstractmethod
from typing import Any, List, Mapping, MutableMapping, Optional, \
    Sequence, \
    Tuple, Union

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql.elements import UnaryExpression

from .container import PagerParams

__all__ = [
    'AbstractPagerViewMixin',
]


class AbstractPagerViewMixin(metaclass=ABCMeta):
    """
    Mixin для постраничной навигации
    """
    @property
    @abstractmethod
    def _get_params(self) -> Any: ...

    @abstractmethod
    def _get_params_getall(self, param: str) -> Sequence[str]: ...

    DEFAULT_LIMIT: Optional[int] = None
    DEFAULT_PAGE: int = 1
    DEFAULT_SORT_BY: Optional[str] = None
    DEFAULT_ASC: str = 'false'
    MAX_LIMIT: int = 1000

    def _get_pager_params(self) -> PagerParams:
        """
        Получение GET параметров, относящихся к пэйджингу

        :return:
        """
        cls = self.__class__
        get_params = self._get_params

        try:
            page = abs(int(get_params.get('page') or 1))

        except (ValueError, TypeError):
            page = cls.DEFAULT_PAGE

        try:
            limit = abs(int(get_params.get('limit')))

            if cls.MAX_LIMIT and limit > cls.MAX_LIMIT:
                limit = cls.MAX_LIMIT

        except (ValueError, TypeError):
            limit = cls.DEFAULT_LIMIT

        start = 0
        if limit:
            start = (page - 1) * limit

        sort_by_params = self._get_params_getall('sort_by')
        sort_by = sort_by_params or cls.DEFAULT_SORT_BY

        asc_params = self._get_params_getall('asc')
        desc_params = self._get_params_getall('desc')
        sort_params = self._get_params_getall('sort')

        asc_list = list(
            itertools.chain.from_iterable([
                [('asc', p) for p in asc_params],
                [('desc', p) for p in desc_params],
                [('sort', p) for p in sort_params],
            ]),
        )[:len(sort_by_params)]

        if len(asc_list) < len(sort_by_params):
            asc_list = asc_list + [
                ('asc', cls.DEFAULT_ASC)
                for _ in range(len(sort_by_params) - len(asc_list))
            ]

        asc = [
            (t == 'asc' and p in ('true', '1', 'yes')) or
            (t == 'desc' and p not in ('true', '1', 'yes')) or
            (t == 'sort' and p not in ('down', 'desc'))
            for t, p in asc_list
        ]

        return PagerParams(
            page=page, start=start, limit=limit, asc=asc, sort_by=sort_by,
        )

    def _handle_pager_params(
        self,
        db_cls: DeclarativeMeta,
        db_joins: MutableMapping[str, str],
        aliased_db_cls: Optional[AliasedClass] = None,
        order_by_map: Optional[
            Mapping[str, Union[UnaryExpression, InstrumentedAttribute]]
        ] = None,
        default_order_by: Optional[
            Sequence[Union[UnaryExpression, InstrumentedAttribute]]
        ] = None,
        except_sort_by: Optional[Sequence[str]] = None,
    ) -> Tuple[int, int, List[UnaryExpression]]:
        """
        Обработка пэйджинга (срез данных для передачи только необходимого).

        :param db_cls: Объект модели sqlalchemy.
        :param db_joins: Словарь стыковки моделей по типу (inner или outer).
        :param aliased_db_cls: Алиса объекта модели (требуется если отношение
        для модели является self-referenced).
        :param order_by_map: Карта, согласно которой нужно подставлять
        order_by параметры на основе параметров GET запроса sort_by
        :param default_order_by: Сортировка по-умолчанию.
        :param except_sort_by: Список вариантов параметра sort_by, которые
        запрещено обрабатывать.
        :return:
        """
        if except_sort_by is None:
            except_sort_by = []

        if default_order_by is None:
            default_order_by = []

        if order_by_map is None:
            order_by_map = {}

        mapper = inspect(db_cls)

        pager_params = self._get_pager_params()
        order_by = default_order_by
        stop = None

        if pager_params.sort_by is not None:
            # управление сортировкой
            sort_by = pager_params.sort_by
            splitted_sort_by = [
                sb.split('.', 1) for sb in sort_by
            ]

            def handle_simple_column(i):
                """
                Обработка сортировки по простой колонке
                :param i: Индекс
                :return:
                """
                if sort_by[i] in order_by_map:
                    return order_by_map[sort_by[i]]

                if sort_by[i] not in mapper.columns.keys():
                    return
                return getattr(db_cls, sort_by[i])

            def handle_relation(i):
                """
                Обработка сортировки по колонке отношения
                :param i: Индекс
                :return:
                """
                if sort_by[i] in order_by_map:
                    return order_by_map[sort_by[i]]

                if splitted_sort_by[i][0] not in mapper.relationships.keys():
                    return

                if splitted_sort_by[i][0] not in db_joins:
                    # join мог быть объявлен ранее
                    db_joins[splitted_sort_by[i][0]] = 'outerjoin'

                rel_cls = mapper.relationships[
                    splitted_sort_by[i][0]
                ].mapper.class_

                if rel_cls is db_cls:
                    rel_cls = aliased_db_cls

                return getattr(rel_cls, splitted_sort_by[i][1])

            order_by = [
                handle_relation(i) if len(splitted_sort_by[i]) == 2 else
                handle_simple_column(i)
                for i in range(len(sort_by))
                if sort_by not in except_sort_by
            ]

            order_by_indexed = list(
                filter(
                    lambda x: x[1] is not None, enumerate(order_by),
                ),
            )

            if not order_by_indexed:
                order_by = default_order_by or [getattr(db_cls, 'id')]
            else:
                order_by = [
                    ob.asc() if pager_params.asc[i] else ob.desc()
                    for i, ob in order_by_indexed
                ]

        if pager_params.start is not None and pager_params.limit:
            # управление величиной среза
            stop = pager_params.start + pager_params.limit

        return pager_params.start or 0, stop, order_by
