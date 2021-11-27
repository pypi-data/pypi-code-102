"""Routines for Chat analysis"""

import numpy as np

from .currency import CurrencyConverter

def sc_currency_stat(msgs, cc):
    assert isinstance(cc, CurrencyConverter)
    
    msgs_paid = [msg for msg in msgs if msg['message_type'] == 'paid_message']

    N_msgs_paid = len(msgs_paid)
    if N_msgs_paid == 0:
        print("No superchat found")
        return None
    
    field_names = ('text','amount','currency','currency_symbol')
    types = ('U20','f4','U3','U3')
    dtype = np.dtype(list(zip(field_names, types)))
    msgs_paid_arr = np.empty((N_msgs_paid,), dtype=dtype)

    for j_msg, msg in enumerate(msgs_paid):
        money = msg['money']
        msgs_paid_arr[j_msg] = tuple((money[k] for k in field_names)) 

    msgs_paid_sorted_cur = np.sort(msgs_paid_arr, order='currency')
    currency_arr = msgs_paid_sorted_cur['currency']



    diff_curr_mask = currency_arr[:-1] != currency_arr[1:]
    diff_curr_indices, = np.where(diff_curr_mask)
    N_currency_tot = len(set(currency_arr))
    indices_srt_curr_arr = np.empty((N_currency_tot,), dtype='i4')
    indices_srt_curr_arr[0] = 0
    indices_srt_curr_arr[1:] = diff_curr_indices + 1
    
    num_curr_arr = np.empty((N_currency_tot,), dtype='i4')
    num_curr_arr[:-1] = np.diff(indices_srt_curr_arr)
    num_curr_arr[-1] = currency_arr.size - indices_srt_curr_arr[-1]

    N_currency = N_currency_tot    

    amount_by_currency_arr = np.empty((N_currency,), dtype=[
        ('currency','U3'),('total_amount','f8'),('total_amount_KRW','f8'),('percentage','f8')])

    for j_currency in range(N_currency):
        j_srt = indices_srt_curr_arr[j_currency]
        j_end = j_srt + num_curr_arr[j_currency]

        seg = currency_arr[j_srt:j_end]
        currency = seg[0]
        assert all([currency == v for v in seg])

        amount_sum = msgs_paid_sorted_cur[j_srt:j_end]['amount'].sum()
        amount_by_currency_arr[j_currency] = (currency, amount_sum, -1., -1.)

        
    for j, (currency, amount, _, _) in enumerate(amount_by_currency_arr):
        amount_by_currency_arr[j]['total_amount_KRW'] = cc.convert(amount, currency)

    total_amount_KRW_sum = amount_by_currency_arr['total_amount_KRW'].sum()

    amount_by_currency_arr['percentage'] = amount_by_currency_arr['total_amount_KRW'] / total_amount_KRW_sum * 100

    sorted_by_amount_arr = np.flip(np.sort(amount_by_currency_arr, order='total_amount_KRW'))
    
    return sorted_by_amount_arr

