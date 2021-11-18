#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore[no-untyped-def]
"""
Test module for testing exchange.Exchange class

Authors:
    Steffen Guenther

Since:
    07.07.2021

Version:
    07.07.2021
"""
import os
import oyaml as yaml
from model.exchange.exchange import Exchange, format_request_url
from model.database.tables import Exchange as ExchangeTable
from model.database.tables import Currency, ExchangeCurrencyPair, Ticker
import _paths  # pylint: disable=unused-import

path = os.getcwd() + "/open_crypto/tests/unit_tests"

with open(path + "/test_file.yaml", "r", encoding="UTF-8") as file:
    test_file: dict = yaml.load(file, Loader=yaml.FullLoader)


class TestExchange:
    """Test class for Exchange."""
    # pylint: disable=too-many-public-methods

    Exchange = Exchange(test_file, None, timeout=10, interval="seconds")

    def test_increase_interval(self) -> None:
        """
        Test function to increase interval from "seconds" to "minutes".
        """
        index = 2
        self.Exchange.interval = self.Exchange.interval_strings[index]
        self.Exchange.increase_interval()
        assert self.Exchange.interval == self.Exchange.interval_strings[index + 1]

    def test_increase_max_interval(self) -> None:
        """
        Test that function can not increase interval higher "days".
        """
        index = - 1
        self.Exchange.interval = self.Exchange.interval_strings[index]
        self.Exchange.increase_interval()
        assert self.Exchange.interval == self.Exchange.interval_strings[index]

    def test_decrease_interval(self) -> None:
        """
        Test function that decreases interval from "hours" to "minutes".
        """
        index = 2
        self.Exchange.interval = self.Exchange.interval_strings[index]
        self.Exchange.decrease_interval()
        assert self.Exchange.interval == self.Exchange.interval_strings[index - 1]

    def test_decrease_min_interval(self) -> None:
        """
        Test that function cannot decrease interval lower than "seconds".
        """
        index = 0
        self.Exchange.interval = self.Exchange.interval_strings[index]
        self.Exchange.decrease_interval()
        assert self.Exchange.interval == self.Exchange.interval_strings[index]

    def test_format_request_url_without_alias(self):
        """
        Test format request_url without alias. Currency-pair is supposed to be in directly in the url.
        """
        request_name = "tickers"
        currency1 = Currency(name="Test1")
        currency2 = Currency(name="Test2")
        exchange = ExchangeTable(name="TestExchange")

        currency_pairs = ExchangeCurrencyPair(first=currency1, second=currency2, exchange=exchange)

        request_urls = self.Exchange.extract_request_urls(test_file["requests"][request_name],
                                                          request_name=request_name,
                                                          request_table=Ticker,
                                                          currency_pairs=currency_pairs)[request_name]

        url, params = format_request_url(request_urls["url"], request_urls["pair_template"], 'test1-test2',
                                         currency_pairs, request_urls["params"])

        assert url == 'https://api.pro.coinbase.com/products/test1-test2/ticker'
        assert params == {}

    def test_format_request_url_with_alias(self):
        """
        Test format request_url with alias. Currency-pair is supposed to be in params.
        """
        request_name = "order_books"  #
        currency1 = Currency(name="Test1")
        currency2 = Currency(name="Test2")
        exchange = ExchangeTable(name="TestExchange")

        currency_pairs = ExchangeCurrencyPair(first=currency1, second=currency2, exchange=exchange)

        request_urls = self.Exchange.extract_request_urls(test_file["requests"][request_name],
                                                          request_name=request_name,
                                                          request_table=Ticker,
                                                          currency_pairs=currency_pairs)[request_name]

        url, params = format_request_url(request_urls["url"], request_urls["pair_template"], 'test1-test2',
                                         currency_pairs, request_urls["params"])

        assert url == 'https://api.pro.coinbase.com/products/book'
        assert params == {'level': 2, 'symbol': 'test1-test2'}

    #
    # def test_sort_order_book(self):
    #     """
    #     # ToDo
    #     """
    #     pass

    # def test_extract_request_urls(self):
    #     """
    #     # ToDo
    #     """
    #     pass
    #
    # def test_apply_currency_pair_format(self):
    #     """
    #     # ToDo
    #     """
    #     pass
    #
    # def test_format_currency_pairs(self):
    #     """
    #     # ToDo
    #     """
    #     pass
    #
    # def test_format_data(self):
    #     """
    #     # ToDo
    #     """
    #     pass
    #
    # def test_request(self):
    #     """
    #     # ToDo
    #     """
    #     pass
