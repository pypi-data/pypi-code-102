import gzip
from urllib import request
from io import StringIO
import pandas as pd

base_url = "https://download.gatedata.org/"


def _deal_with_month_day(date: int):
    if len(str(date)) == 1:
        return '0' + str(date)
    else:
        return str(date)


def _get_full_url(biz, market, type, year, month, day='', hour=''):
    """
    futures_usdt/trades/202110/ETH_USD-202110.csv.gz
    """
    month = _deal_with_month_day(month)
    day = _deal_with_month_day(day)
    hour = _deal_with_month_day(hour)

    url_params_string = f"{biz}/{type}/{year}{month}/{market}-{year}{month}{day}{hour}.csv.gz"

    return base_url + url_params_string


def _get_headers(biz, type):
    if type.startswith('candlesticks'):
        type = 'kline'

    usdt_swap = dict(
        trades=['timestamp', 'tradeid', 'price', 'size'],
        mark_prices=['timestamp', 'index_price', 'mark_price', 'last_price'],
        kline=['timestamp', 'size', 'close', 'high', 'low', 'open'],
        funding_applies=['timestamp', 'funding_rate'],
        funding_updates=['timestamp', 'funding_rate', 'interest_rate', 'bid_diff', 'ask_diff', 'mark_price',
                         'index_price', 'update_count'],
        orderbooks=['timestamp', 'action', 'price', 'size', 'orderid', 'merged_count'],
    )

    spot = dict(
        deals=['timestamp', 'tradeid', 'price', 'size', 'side'],
        kline=['timestamp', 'size', 'close', 'high', 'low', 'open'],
        orderbooks=['timestamp', 'action', 'price', 'size', 'orderid', 'merged_count'],
    )

    header_dict = {
        'spot': spot,
        'futures_btc': usdt_swap,
        'futures_usdt': usdt_swap
    }

    return header_dict[biz][type]


def how():
    print("5 - 7 params:")
    print("biz \t->\t spot futures_btc futures_usdt")
    print("market \t->\t BTC_USDT ....")
    print("type \t->\t trades/deals mark_prices candlesticks_10s funding_applies")
    print("    \t\tfunding_updates orderbooks")
    print("year \t->\t 2021")
    print("month \t->\t 11")
    print("day \t->\t 17 (only in orderbooks)")
    print("hour \t->\t 15 (only in orderbooks)")

def get(biz, market, type, year, month, day='', hour=''):

    file_url = _get_full_url(biz, market, type, year, month, day, hour)
    print(file_url)
    response = request.urlopen(file_url)
    uncom = gzip.GzipFile(fileobj=response)
    data_string = StringIO(uncom.read().decode())

    dataframe = pd.read_csv(data_string, header=None)
    dataframe.columns = _get_headers(biz, type)

    return dataframe