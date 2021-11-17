import unittest
from tests.conftest import *


class TestAcctPayment(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)

        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_payment_create(self):
        result = dg_sdk.AcctPayment.create(ord_amt="0.01",
                                           acct_split_bunch="{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000109133323\"}]}",
                                           good_desc="good_desc")

        assert result["resp_code"] == "10000000"

    def test_payment_query(self):
        result = dg_sdk.AcctPayment.create(ord_amt="0.01",
                                           acct_split_bunch="{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000109133323\"}]}",
                                           good_desc="good_desc")

        result = dg_sdk.AcctPayment.query(org_req_date=result["req_date"], org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "20000004"

    def test_payment_refund(self):
        result = dg_sdk.AcctPayment.create(ord_amt="0.01",
                                           acct_split_bunch="{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000109133323\"}]}",
                                           good_desc="good_desc")

        result = dg_sdk.AcctPayment.refund(ord_amt="0.01", org_req_date=result["req_date"],
                                           org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "20000004"

    def test_payment_refund_query(self):
        result = dg_sdk.AcctPayment.create(ord_amt="0.01",
                                           acct_split_bunch="{\"acct_infos\":[{\"div_amt\":\"0.01\",\"huifu_id\":\"6666000109133323\"}]}",
                                           good_desc="good_desc")
        result = dg_sdk.AcctPayment.refund(ord_amt="0.01",org_req_date=result["req_date"], org_req_seq_id=result["req_seq_id"])
        result = dg_sdk.AcctPayment.refund_query(org_req_date=result["req_date"], org_req_seq_id=result["req_seq_id"])

        assert result["resp_code"] == "00000100"

    def test_payment_balance_query(self):
        result = dg_sdk.AcctPayment.balance_query()

        assert result["resp_code"] == "00000000"
