from typing import Final, Iterable, Literal, Union
from urllib.parse import urlsplit

import httpx

from . import schema

Action = Literal["adjust", "allocate", "deallocate", "receive", "release"]
post_headers: Final = {"Content-Type": "application/json", "Accept": "application/json"}


class Inventory:
    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    def list_available_stock(
        self, warehouse_code: str, skus: Iterable[str], limit: int = 100
    ) -> Iterable[schema.Stock]:
        skus_query = "&".join(f"sku={sku}" for sku in skus)
        next_page = (
            f"/private/v1/inventory/{warehouse_code}/?{skus_query}&limit={limit}"
        )
        while True:
            response = self.client.get(
                next_page, headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            data = schema.PaginatedStockList.parse_obj(response.json())
            yield from data.results or []

            next_page = (
                "{0.path}?{0.query}".format(urlsplit(data.next)) if data.next else ""
            )
            if not next_page:
                break

    def _post_quantity(
        self,
        action: Action,
        warehouse_code: str,
        data: Union[schema.SKUQuantity, schema.PositiveSKUQuantity],
    ) -> None:
        self.client.post(
            f"/private/v1/inventory/{warehouse_code}/{action}/",
            content=data.json(exclude_none=True),
            headers=post_headers,
        ).raise_for_status()

    # Action methods below could really use functools.partialmethod. Mypy doesn't like
    # that though. See:
    # -> https://github.com/python/mypy/issues/1484
    # -> https://github.com/python/mypy/issues/2967
    # -> https://github.com/python/mypy/issues/8619
    def adjust(self, warehouse_code: str, data: schema.SKUQuantity) -> None:
        self._post_quantity("adjust", warehouse_code, data)

    def allocate(self, warehouse_code: str, data: schema.PositiveSKUQuantity) -> None:
        self._post_quantity("allocate", warehouse_code, data)

    def deallocate(self, warehouse_code: str, data: schema.PositiveSKUQuantity) -> None:
        self._post_quantity("deallocate", warehouse_code, data)

    def receive(self, warehouse_code: str, data: schema.PositiveSKUQuantity) -> None:
        self._post_quantity("receive", warehouse_code, data)

    def release(self, warehouse_code: str, data: schema.PositiveSKUQuantity) -> None:
        self._post_quantity("release", warehouse_code, data)
