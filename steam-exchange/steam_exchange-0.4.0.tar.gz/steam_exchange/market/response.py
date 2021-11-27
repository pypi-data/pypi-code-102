import json
import re

import requests

from steam_exchange.util.price import Price
from steam_exchange.util.time import parse_time_str


class Response:
    def __init__(self, resp: requests.Response):
        self.response = resp


class ItemNameIdResponse(Response):
    regex = re.compile(r"Market_LoadOrderSpread\(\s*(\d+)\s*\)")

    def __init__(self, resp):
        super().__init__(resp)
        match = self.regex.search(resp.text)
        if match:
            self.name_id = int(match.group(1))
        else:
            raise NotImplementedError()

    def __str__(self):
        return "ItemNameIdResponse{{id={}}}".format(self.name_id)


class PriceQuantity:
    def __init__(self, level):
        self.price = Price(level[0])
        self.quantity = level[1]

    def __str__(self):
        return "{{{} @ {}}}".format(self.quantity, self.price)


class ItemOrdersHistogramResponse(Response):
    TOP_ORDER_COUNT = 5

    def __init__(self, resp):
        super().__init__(resp)
        resp = resp.json()
        self.highest_buy_order = Price(resp["highest_buy_order"])
        self.lowest_sell_order = Price(resp["lowest_sell_order"])
        self.highest_buy_order.value = self.highest_buy_order.value / 100
        self.lowest_sell_order.value = self.lowest_sell_order.value / 100
        self.buys = []
        self.sells = []
        for level in resp["buy_order_graph"]:
            self.buys.append(PriceQuantity(level))
        for level in resp["sell_order_graph"]:
            self.sells.append(PriceQuantity(level))
        self._normalise_levels(self.buys)
        self._normalise_levels(self.sells)
        self.buys_count = sum(pq.quantity for pq in self.buys)
        self.sells_count = sum(pq.quantity for pq in self.sells)

    def _normalise_levels(self, levels):
        previous_level_quantity = 0
        for level in levels:
            this_level_quantity = level.quantity - previous_level_quantity
            previous_level_quantity = level.quantity
            level.quantity = this_level_quantity

    def __str__(self):
        top_buys = ", ".join(
            str(pq) for pq in self.buys[: self.TOP_ORDER_COUNT]
        )
        top_sells = ", ".join(
            str(pq) for pq in self.sells[: self.TOP_ORDER_COUNT]
        )
        return "ItemOrdersHistogramResponse{{best_buy={}, best_sell={}, buys={}, top_buys={}, sells={}, top_sells={}}}".format(
            self.highest_buy_order,
            self.lowest_sell_order,
            self.buys_count,
            top_buys,
            self.sells_count,
            top_sells,
        )


class ItemPricingResponse(Response):
    def __init__(self, resp):
        super().__init__(resp)
        resp = resp.json()
        self.lowest_price = Price.parse(resp["lowest_price"])
        self.volume = resp["volume"]
        self.median_price = Price.parse(resp["median_price"])

    def __str__(self):
        return "ItemPricingResponse{{lowest_price={}, volume={}, median_price={}}}".format(
            self.lowest_price, self.volume, self.median_price
        )


class MedianSaleHistory:
    def __init__(self, time, price, quantity):
        if type(time) is str:
            self.time = parse_time_str(time)
        else:
            self.time = time
        self.price = Price(
            price, "USD"
        )  # The price is in USD unless you have the steamLoginSecure cookie set
        self.quantity = quantity

    def __str__(self):
        return f"[{self.time},{self.price},{self.quantity}]"


class SalesHistoryResponse(Response):
    delim_start = "var line1="
    delim_end = ";"

    def __init__(self, resp):
        super().__init__(resp)
        start = resp.text.find(self.delim_start)
        end = resp.text.find(self.delim_end, start)
        text = resp.text[start + len(self.delim_start): end]
        jobj = json.loads(text)
        self.items = self.parse_json(jobj)

    @staticmethod
    def parse_json(jobj):
        return [MedianSaleHistory(arr[0], arr[1], arr[2]) for arr in jobj]

    def __str__(self):
        return ",".join(str(x) for x in self.items[:10])


class CreateListingResponse(Response):
    def __init__(self, resp: requests.Response):
        super().__init__(resp)


class RemoveListingResponse(Response):
    def __init__(self, resp: requests.Response):
        super().__init__(resp)
        self.ok = resp.ok
