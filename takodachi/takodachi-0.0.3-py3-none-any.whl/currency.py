"""Currency"""

import requests

class CurrencyConverter(object):
    url_form = 'https://api.exchangerate-api.com/v4/latest/{}'
    def __init__(self, base):
        assert len(base) and (type(base) is str)
        self.url = self.__class__.url_form.format(base)
        self.data = requests.get(self.url).json()
        self.base = base
        
    def convert(self, amount, currency):
        rate = self.data['rates'].get(currency)
        if rate is None: raise Exception("Unable to recognize currency : '{}'".format(currency))
        amount_in_base = amount / rate
        return amount_in_base

