from .constants.apps import CSGO
from .engine.engine import Engine
from .engine.session import Session
from .market.request import (
    ItemNameId,
    ItemOrdersHistogram,
    ItemPricing,
    SaleHistory,
)


def _main():
    e = Engine(Session.load_from_file("session.json"))
    # print(e.request(ItemPricing(CSGO, 'Clutch Case')))
    # print(e.request(ItemNameId(CSGO, 'Clutch Case')))
    # print(e.request(ItemOrdersHistogram(176241017)))
    print(e.request(SaleHistory(CSGO, "Clutch Case")))


if __name__ == "__main__":
    _main()
