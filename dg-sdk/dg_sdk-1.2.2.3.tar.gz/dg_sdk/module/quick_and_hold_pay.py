from dg_sdk.module.request_tools import request_post, card_bind_confirm, card_bind_apply, \
    card_payment_confirm, card_payment_page_pay, card_payment_apply, card_payment_page_pay, \
    card_payment_sms, card_un_bind, online_payment_query, online_payment_refund, \
    online_payment_refund_query

from dg_sdk.common_util import generate_mer_order_id, generate_req_date
from dg_sdk.dg_client import DGClient
from dg_sdk.module.card import Card
from dg_sdk.module.cert import Cert


class QuickAndHoldPay(object):
    """
    快捷支付与代扣相关接口，
    支付申请，首次四要素验证+发短信
    快捷支付确认
    快捷/代扣绑卡申请接口
    快捷/代扣绑卡确认接口
    快捷代扣解绑
    快捷代扣短信重发时使用
    快捷页面版
    代扣
    线上交易查询
    扫码交易列表查询
    退款
    退款查询
    线上快捷代扣用户注册接口
    """

    @classmethod
    def apply(cls, trans_amt, user_huifu_id, card_bind_id, **kwargs):
        """
        支付申请，首次四要素验证+发短信
        :param trans_amt: 交易金额
        :param user_huifu_id: 用户客户号
        :param card_bind_id: 绑卡ID
        :param kwargs: 非必填额外参数
        """
        required_params = {
            "trans_amt": trans_amt,
            "user_huifu_id": user_huifu_id,
            "card_bind_id": card_bind_id

        }

        required_params.update(kwargs)

        return request_post(card_payment_apply, required_params)

    @classmethod
    def bind_card(cls, merch_name, out_cust_id, card_info: Card, cert_info: Cert, **kwargs):
        """
        快捷/代扣绑卡申请接口
        :param merch_name:商户名称
        :param out_cust_id:顾客用户号
        :param card_info:银行卡信息
        :param cert_info:证件信息
        :param kwargs: 非必填额外参数
        :return: 绑卡接口返回
        """
        required_params = {
            "merch_name": merch_name,
            "out_cust_id": out_cust_id,
            "card_id": card_info.card_id,
            "card_name": card_info.card_name,
            "card_mp": card_info.card_id,
            "vip_code": card_info.vip_code,
            "expiration": card_info.expiration,
            "cert_type": cert_info.cert_type,
            "cert_id": cert_info.cert_id,
            "cert_validity_type": cert_info.cert_validity_type,
            "cert_begin_date": cert_info.cert_begin_date,
            "cert_end_date": cert_info.cert_end_date,

        }

        if not kwargs.get("order_id"):
            required_params["order_id"] = generate_mer_order_id()
        if not kwargs.get("order_date"):
            required_params["order_date"] = generate_req_date()
        if not kwargs.get("product_id"):
            required_params["product_id"] = DGClient.mer_config.product_id

        required_params.update(kwargs)

        return request_post(card_bind_apply, required_params)

    @classmethod
    def bind_card_confirm(cls, merch_name, out_cust_id, auth_code, notify_url, **kwargs):
        """
        快捷/代扣绑卡确认接口
        :param huifu_id: 商户号
        :param trans_amt: 交易金额
        :param goods_desc: 商品描述
        :param auth_code: 支付码
        :param notify_url: 异步回调地址（virgo://http://www.xxx.com/getResp）
        :param kwargs: 非必填额外参数
        :return: 支付结果
        """
        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "merch_name": merch_name,
            "out_cust_id": out_cust_id,
            "notify_url": notify_url
        }

        if not kwargs.get("order_id"):
            required_params["order_id"] = generate_mer_order_id()
        if not kwargs.get("order_date"):
            required_params["order_date"] = generate_req_date()
        if not kwargs.get("product_id"):
            required_params["product_id"] = DGClient.mer_config.product_id

        required_params.update(kwargs)
        return request_post("/ssproxy/verifyCardConfirm", required_params)

    @classmethod
    def un_bind(cls, huifu_id, org_req_date, **kwargs):
        """
        快捷/代扣解绑接口
        :param huifu_id: 商户号
        :param org_req_date: 原始订单请求时间
        :param kwargs: 非必填额外参数
        :return: 支付对象
        """

        required_params = {
            "huifu_id": huifu_id,
            "req_date": org_req_date,
        }
        # sys_id 不传默认用SDK 初始化时配置信息，没有配置，使用商户号
        if not kwargs.get("sys_id"):
            mer_config = DGClient.mer_config
            sys_id = mer_config.sys_id
            if len(mer_config.sys_id) == 0:
                sys_id = huifu_id

            required_params["sys_id"] = sys_id

        required_params.update(kwargs)
        return request_post("/ssproxy/unBind", required_params)

    @classmethod
    def confirm(cls, sms_code, req_date, req_seq_id, goods_desc, **kwargs):
        """
        快捷支付确认
        :param sms_code: 短信验证码
        :param req_date: 原快捷支付申请请求时间
        :param req_seq_id: 原快捷支付申请请求序列号
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "sms_code": sms_code,
            "goods_desc": goods_desc,
            "req_date": req_date,
            "req_seq_id": req_seq_id
        }

        required_params.update(kwargs)
        return request_post(card_payment_confirm, required_params)

    @classmethod
    def sms_code(cls, sms_code, req_date, req_seq_id, goods_desc, **kwargs):
        """
        快捷代扣短信重发时使用
        :param sms_code: 短信验证码
        :param req_date: 原快捷支付申请请求时间
        :param req_seq_id: 原快捷支付申请请求序列号
        :param kwargs: 非必填额外参数
        :return:
        """
        required_params = {
            "sms_code": sms_code,
            "goods_desc": goods_desc,
            "req_date": req_date,
            "req_seq_id": req_seq_id
        }

        required_params.update(kwargs)
        return request_post(card_payment_confirm, required_params)

    @classmethod
    def page(cls, trans_amt, **kwargs):
        """
        快捷支付页面版
        :param trans_amt: 交易金额
        :param kwargs: 非必填额外参数
        """
        required_params = {
            "trans_amt": trans_amt,
        }

        required_params.update(kwargs)

        return request_post(card_payment_page_pay, required_params)

    @classmethod
    def with_hold_pay(cls, trans_amt, **kwargs):
        """
        代扣
        :param trans_amt: 交易金额
        :param kwargs: 非必填额外参数
        """
        required_params = {
            "trans_amt": trans_amt,
        }

        required_params.update(kwargs)

        return request_post(card_payment_page_pay, required_params)

    @classmethod
    def query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", pay_type="", **kwargs):
        """
        线上交易查询接口
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始订单请求时间
        :param pay_type: 原交易支付类型, 快捷支付传quick_pay
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
            "pay_type": pay_type
        }

        required_params.update(kwargs)

        return request_post(online_payment_query, required_params)

    @classmethod
    def query_list(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", pay_type="", **kwargs):
        """
        扫码交易列表查询
        TODO
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始订单请求时间
        :param pay_type: 原交易支付类型, 快捷支付传quick_pay
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
            "pay_type": pay_type
        }

        required_params.update(kwargs)

        return request_post(online_payment_query, required_params)

    @classmethod
    def refund(cls, ord_amt, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        线上退款接口
        :param ord_amt: 退款金额
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始订单请求时间
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """

        required_params = {
            "ord_amt": ord_amt,
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
        }

        required_params.update(kwargs)

        return request_post(online_payment_refund, required_params)

    @classmethod
    def refund_query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        线上退款查询接口
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始退款请求时间
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
        }
        required_params.update(kwargs)
        return request_post(online_payment_refund_query, required_params)

    @classmethod
    def customer_reg(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        线上快捷代扣用户注册接口
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始退款请求时间
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        :return: 返回报文
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
        }
        required_params.update(kwargs)
        return request_post(online_payment_refund_query, required_params)
