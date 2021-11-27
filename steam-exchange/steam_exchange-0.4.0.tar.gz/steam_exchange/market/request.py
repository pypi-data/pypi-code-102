import requests

from steam_exchange.config.config import (
    DEFAULT_COUNTRY,
    DEFAULT_CURRENCY,
    DEFAULT_LANGUAGE,
)
from steam_exchange.constants.currency import CURRENCY_CODE_MAP
from steam_exchange.engine.request import Request
from steam_exchange.util.price import Price

from .response import (
    CreateListingResponse,
    ItemNameIdResponse,
    ItemOrdersHistogramResponse,
    ItemPricingResponse,
    RemoveListingResponse,
    SalesHistoryResponse,
)


# Translates a name into an ID
class ItemNameId:
    BASE_URL = "https://steamcommunity.com/market/listings/{appid}/{item}"

    def __init__(self, appid, item_name):
        self.appid = appid
        self.item_name = item_name

    def build_request(self, session):
        return Request(
            self.BASE_URL.format(appid=self.appid, item=self.item_name)
        )

    def response(self, resp):
        return ItemNameIdResponse(resp)


# Gets the current orderbook for an item
class ItemOrdersHistogram:
    BASE_URL = "https://steamcommunity.com/market/itemordershistogram?country={country}&language={language}&currency={currency}&item_nameid={item_nameid}&two_factor=0"

    def __init__(self, item_nameid):
        self.country = DEFAULT_COUNTRY
        self.currency = CURRENCY_CODE_MAP[DEFAULT_CURRENCY]
        self.language = DEFAULT_LANGUAGE
        self.item_nameid = item_nameid

    def build_request(self, session):
        return Request(
            self.BASE_URL.format(
                country=self.country,
                language=self.language,
                currency=self.currency,
                item_nameid=self.item_nameid,
            )
        )

    def response(self, resp):
        return ItemOrdersHistogramResponse(resp)


# Gets volume and price overview
class ItemPricing:
    BASE_URL = "https://steamcommunity.com/market/priceoverview/?appid={appid}&currency={currency}&market_hash_name={item}"

    def __init__(self, appid, item_name):
        self.appid = appid
        self.currency = CURRENCY_CODE_MAP[DEFAULT_CURRENCY]
        self.item_name = item_name

    def build_request(self):
        return Request(
            self.BASE_URL.format(
                appid=self.appid, currency=self.currency, item=self.item_name
            )
        )

    def response(self, resp):
        return ItemPricingResponse(resp)


# Gets the median sales prices of an item
class SaleHistory:
    BASE_URL = "https://steamcommunity.com/market/listings/{appid}/{item}"

    def __init__(self, appid, item_name):
        self.appid = appid
        self.item_name = item_name

    def build_request(self, session):
        return Request(
            self.BASE_URL.format(appid=self.appid, item=self.item_name)
        )

    def response(self, resp):
        return SalesHistoryResponse(resp)


class CreateListing:
    # POST, requires session, + payload
    BASE_URL = "https://steamcommunity.com/market/sellitem/"
    PAYLOAD = "sessionid={session_id}&appid={appid}&contextid={context_id}&assetid={asset_id}&amount={amount}&price={price}"

    def __init__(self, appid, session_id, asset_id, price: Price):
        self.appid = appid
        self.session_id = session_id
        self.asset_id = asset_id
        self.price = price
        self.context_id = "2"
        self.amount = 1

    def build_request(self, session):
        return Request(
            method="POST",
            url=self.BASE_URL,
            payload=self.BASE_URL.format(
                session_id=session.session_id,
                appid=self.appid,
                context_id=self.context_id,
                asset_id=self.asset_id,
                amount=self.amount,
                price=self.price.to_network_format(),
            ),
            headers={
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
            },
        )

    def response(self, resp: requests.Response):
        return CreateListingResponse(resp)


class RemoveListing:
    # POST, requires session
    BASE_URL = "https://steamcommunity.com/market/removelisting/{listing}"

    def __init__(self, listing):
        self.listing = listing

    def build_request(self, session):
        return Request(
            method="POST", url=self.BASE_URL.format(listing=self.listing)
        )

    def response(self, resp: requests.Response):
        return RemoveListingResponse(resp)
