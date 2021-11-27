from typing import Any, Callable, MutableMapping, Optional, Sequence
from urllib.parse import unquote

import ujson

__all__ = [
    'param_setter_factory',
    'json_param_normalizer_factory',
]


def param_setter_factory(
    filled_obj: MutableMapping,
    val_preparer: Optional[Callable[[Any], Any]] = None,
) -> Callable[[str, Any], None]:
    """
    Фабрика для настройки функции аггрегирования параметров определенного
    типа в объект.

    :param filled_obj: объект, в который аггрегируются параметры
    :param val_preparer: функция для подготовки/валидации значения
    :return:
    """
    def obj_filler(col_name: str, val: Any) -> None:
        """
        Установка параметра согласно его наименованию. Для
        сложных аттрибутов (через точку) происходит группировка по
        префиксу до точки.

        :param col_name: наименование колонки (из GET-параметра)
        :param val: значение колонки
        :return:
        """
        splited_column_name = col_name.split('.', 1)
        if val_preparer:
            val = val_preparer(val)

        if len(splited_column_name) == 1:
            # простая колонка
            filled_obj[col_name] = val
            return

        # сложная колонка с префиксом. данный фильтр группируется по
        # префиксу
        if splited_column_name[0] not in filled_obj:
            filled_obj[splited_column_name[0]] = {}

        filled_obj[splited_column_name[0]][splited_column_name[1]] = val

    return obj_filler


def json_param_normalizer_factory(
    column_names: Sequence[str],
) -> Callable[[Any, Callable[[str, Any], None]], bool]:
    """
    Фабрика для нормализации параметра, который может быть строкой или
    json url-encoded массивом

    :param column_names: имена колонок, переданные в запросе
    :return:
    """
    def value_transformer(
        param_value: Any,
        setter: Callable[[str, Any], None],
    ) -> bool:
        # парсинг search параметра
        try:
            search_list = ujson.loads(unquote(param_value))
            if not isinstance(search_list, list):
                raise ValueError

        except (TypeError, ValueError):
            for column_name in column_names:
                setter(column_name, param_value)

            return False

        for index, column_name in enumerate(column_names):
            try:
                value = search_list[index]
                if not value:
                    continue

                setter(column_name, value)

            except IndexError:
                pass

        return True

    return value_transformer
