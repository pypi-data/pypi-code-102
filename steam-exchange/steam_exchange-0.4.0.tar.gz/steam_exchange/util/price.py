from decimal import ROUND_DOWN, Decimal

from steam_exchange.config.config import DEFAULT_CURRENCY
from steam_exchange.constants.fees import APP_FEES, STEAM_FEE, STEAM_PERCENT_FEE

STEAM_PREFIXES = {
    "A$ ": "AUD",
}

CURRENCY_PREFIX = {"AUD": "A$", "USD": "$"}


class Price:
    @staticmethod
    def parse(price):
        for pfx in STEAM_PREFIXES:
            if price.startswith(pfx):
                return Price(price[len(pfx):], STEAM_PREFIXES[pfx])
        raise NotImplementedError()

    def __init__(self, value, currency=None):
        self._value = Decimal(value).quantize(
            Decimal("0.01"), rounding=ROUND_DOWN
        )
        if currency:
            self._currency = currency
        else:
            self._currency = DEFAULT_CURRENCY

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def currency(self):
        return self._currency

    def to_network_format(self):
        return str((self._value * 100).to_integral_value())

    def __str__(self):
        pfx = CURRENCY_PREFIX[self.currency]
        return "{}{}".format(pfx, self.value)


def _get_market_fees(app_fee=None, app=None):
    if app_fee is None:
        if app is None:
            raise RuntimeError("Missing argument")
        app_fee = APP_FEES[app]
    return app_fee


def calculate_seller_price(market_price, app_fee=None, app=None):
    percent_fee = STEAM_PERCENT_FEE + _get_market_fees(app_fee, app)
    return (market_price / percent_fee) - STEAM_FEE


def calculate_market_price(seller_price, app_fee=None, app=None):
    percent_fee = STEAM_PERCENT_FEE + _get_market_fees(app_fee, app)
    return percent_fee * (seller_price + STEAM_FEE)
