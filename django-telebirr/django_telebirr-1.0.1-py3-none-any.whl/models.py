from django.db import models
from uuid import uuid4


NULL = {'null': True, 'blank': True}


class TelebirrMixin(models.Model):
    id = models.UUIDField(default=uuid4)
    receive_name = models.CharField(max_length=255, default='Ashewa technology')
    short_code = models.CharField(max_length=100)
    subject = models.CharField(max_length=500)
    amount = models.PositiveIntegerField(default=0)
    out_trade_no = models.CharField(max_length=255)

    phone = models.CharField(max_length=20, **NULL)
    trade_no = models.CharField(max_length=100, **NULL)
    transaction_no = models.CharField(max_length=100, **NULL)
    pay_url = models.URLField(**NULL)

    paid = models.BooleanField(default=False)

    class Meta:
        abstract = True
