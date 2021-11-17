from typing import Optional

from MSApi.Assortment import Assortment
from MSApi.mixin import AttributeMixin, SalePricesMixin
from MSApi.mixin.ProductfolderMixin import ProductfolderMixin
from MSApi.mixin.RequestByIdMixin import RequestByIdMixin
from MSApi.mixin.GenListMixin import GenerateListMixin


class Service(Assortment,
              AttributeMixin,
              ProductfolderMixin,
              SalePricesMixin,
              RequestByIdMixin,
              GenerateListMixin):

    _type_name = 'service'
