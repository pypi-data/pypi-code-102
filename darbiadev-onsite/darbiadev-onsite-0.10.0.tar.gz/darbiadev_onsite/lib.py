#!/usr/bin/env python

import jaydebeapi
from importlib.resources import files
from typing import Any


class OnSiteServices:
    """A class wrapping an ODBC connection to OnSite.

    This class wraps an ODBC connection to OnSite.
    """

    def __init__(
            self,
            connection_url: str,
            username: str,
            password: str
    ):
        self._connection_url: str = connection_url
        self.__username: str = username
        self.__password: str = password

    def _connect(
            self,
    ):
        return jaydebeapi.connect(
            "com.filemaker.jdbc.Driver",
            self._connection_url,
            [self.__username, self.__password],
            str(files("darbiadev_onsite").joinpath("vendor/fmjdbc.jar")),
        )

    def _make_query(
            self,
            sql: str,
    ) -> list[dict[str, Any]]:
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(sql)

            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_order(
            self,
            order_number: int,
    ) -> dict[str, Any]:
        order_data = self._make_query(sql=_get_sql("order.sql", order_number=order_number))[0]
        order_data["lines"] = self._make_query(sql=_get_sql("linesoe.sql", order_number=order_number))
        order_data["addresses"] = self._make_query(sql=_get_sql("address.sql", order_number=order_number))
        order_data["packages"] = self._make_query(sql=_get_sql("packimport.sql", order_number=order_number))
        order_data["events"] = self._make_query(sql=_get_sql("events.sql", order_number=order_number))

        return order_data

    def get_design_title(
            self,
            design_number: int,
    ) -> str:
        design_data = self._make_query(sql=_get_sql("design_title.sql", design_number=design_number))[0]

        return design_data["DesignName"]

    def get_designs_for_customer_purchase_order(
            self,
            customer_purchase_order: str,
    ) -> list[str]:
        designs = self._make_query(sql=_get_sql("designs_for_po.sql", customer_purchase_order=customer_purchase_order))

        return [str(int(dct["id_Design"])) for dct in designs]


def _get_sql(
        file_name: str,
        **kwargs: str
) -> str:
    path = str(files("darbiadev_onsite").joinpath(f"sql/{file_name}"))
    sql = open(path).read()
    return sql.format(**kwargs)
