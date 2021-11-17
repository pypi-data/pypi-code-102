import datetime
from decimal import Decimal
from collections import defaultdict

from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

from ..core.constants import PayType
from ..core.constants import ShippingPartnerCodes_DICT
from ..core.base_models import BaseModelTimeAndDeleted
from ..core.model_function import get_object_or_None
from ..core.common_utils import get_uuid4_hex
from ..sparrow_orders.constants import AftersaleFinanceStatus
from ..sparrow_orders.constants import RefundStatus
from ..sparrow_orders.constants import AftersaleStatus
from ..sparrow_orders.constants import AftersaleFinanceType
from ..sparrow_orders.constants import AftersaleSource
from ..sparrow_orders.constants import CancelSource
from ..sparrow_orders.constants import AftersaleActions
from ..sparrow_orders.constants import CouponSource
from ..sparrow_orders.constants import AfterSaleType
from ..sparrow_orders.constants import PayStepType
from ..sparrow_orders.constants import PayMethod
from ..sparrow_orders.models import generate_aftersale_number
from ..sparrow_orders.models import OrderPayment
from ..sparrow_orders.models import Order
from ..sparrow_orders.models import Line
from ..sparrow_orders.models import LineOrderPromotion
from ..sparrow_distribute.constants import DistributeStatus
from ..sparrow_promotions.models import Coupon
from .constants import Aftersale_Number_Refund_Status
from . import APP_LABEL


class Afs(BaseModelTimeAndDeleted):
    '''
    售后单
    和 Line 是多对多的关系
    和 Order 是多对一的关系

    attr startwith "_batch" such as "_batch_line_after_sales" is a trick for batch operation
    '''

    AFTERSALE_FINANCE_STATUS_CHOICES = (
        (AftersaleFinanceStatus.INIT, "财务未审"),
        (AftersaleFinanceStatus.APPROVED_1ST, "财务一审通过，待二审"),
        (AftersaleFinanceStatus.APPROVED, "财务二审通过"),
        (AftersaleFinanceStatus.REJECTED, "财务驳回")
    )
    REFUND_STATUS_CHOICES = (
        (RefundStatus.INIT, "未退款"),
        (RefundStatus.SUCCEEDED, "退款成功"),
        (RefundStatus.FAILED, "退款失败")
    )
    AFTERSALE_FINANCE_TYPE_CHOICES = (
        (AftersaleFinanceType.AUTO, "正常退单"),
        (AftersaleFinanceType.MANUAL, "需要财务手动调账退款"),
    )
    AFTERSALE_SOURCE_CHOICES = (
        (AftersaleSource.GUEST_INITIATED, "客人发起"),
        (AftersaleSource.SERVICE_INITIATED, "客服发起"),
    )
    CANCEL_SOURCE_CHOICES = (
        (CancelSource.GUEST_CANCEL, "客人取消"),
        (CancelSource.SERVICE_CANCEL, "客服取消"),
        (CancelSource.TIMEOUT_CANCEL, "超时自动取消"),
    )
    AFTERSALE_TYPE_CHOICES = (
        (AfterSaleType.NORMAL, "正常退款"),
        (AfterSaleType.EXCHANGE, "换货"),
        (AfterSaleType.COMPLAINT, "投诉"),
        (AfterSaleType.REMINDER, "提醒发货"),
        (AfterSaleType.ONLY_REFUND_POSTAGE, "仅退运费"),
        (AfterSaleType.OTHER, "其他"),
    )
    number = models.CharField(
        "退单号", max_length=128, db_index=True,
        unique=True, default=generate_aftersale_number)
    order_id = models.PositiveIntegerField('Order ID', blank=True,
                                           null=True, db_index=True)
    # order_number (订单编码)
    order_number = models.CharField('Order Number', max_length=128, blank=True, null=True, db_index=True)

    status = models.CharField(
        "Status",
        max_length=128,
        choices=AftersaleStatus.AFTERSALE_STATUS_CHOICES,
        blank=True,
        null=True,
        default=AftersaleStatus.OPEN)
    reason = models.CharField("reason", max_length=512, blank=True)
    postage = models.DecimalField("退的邮费", decimal_places=2, max_digits=12, default=0)
    creator_id = models.CharField(
        'Creator User Id', max_length=100, blank=True, null=True, db_index=True)
    created_time = models.DateTimeField("Date Created", auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", auto_now=True)
    operator_approve_time = models.DateTimeField("客服提交财务的时间", blank=True, null=True, db_index=True)
    # 财务审核的时间，可能是通过也可能是拒绝
    finance_approve_time = models.DateTimeField("财务二审通过的时间", blank=True, null=True, db_index=True)
    finance_approver_id = models.CharField(
        '财务二审人ID', max_length=100, blank=True, null=True, db_index=True)
    # finance_first_approve_time = models.DateTimeField("财务一审通过的时间", blank=True, null=True, db_index=True)
    # finance_first_approver_id = models.CharField(
    #     '财务一审人ID', max_length=100, blank=True, null=True, db_index=True)
    finance_status = models.CharField(
        "财务审核状态",
        max_length=128,
        choices=AFTERSALE_FINANCE_STATUS_CHOICES,
        blank=True,
        null=True,
        default=AftersaleFinanceStatus.INIT)
    finance_reject_reason = models.CharField("财务拒绝理由", max_length=512,
                                             blank=True, null=True)
    # 退款状态
    refund_status = models.CharField(
        "退款状态",
        max_length=128,
        choices=REFUND_STATUS_CHOICES,
        blank=True,
        null=True,
        default=RefundStatus.INIT)
    # 财务要的退款时间，找财务确认是要发起微信退款的时间还是微信退款到账的时间
    # 应该是调起微信退款接口的时间
    refund_time = models.DateTimeField("发起退款的时间", blank=True, null=True, db_index=True)
    # 收到推送退款成功的时间，一期就是收到微信通知成功的时间
    refund_notified_time = models.DateTimeField("退款收到推送的时间", blank=True, null=True, db_index=True)
    # 售后单同步信息
    sync_status = models.BooleanField('同步状态', default=False)
    sync_time = models.DateTimeField('售后单同步时间', null=True, blank=True)
    store_reject_reason = models.CharField("店内系统拒绝理由", max_length=512,
                                           blank=True, null=True)
    # 客服给退单的备注
    operator_note = models.CharField(
        "客服备注", max_length=512,
        blank=True, null=True)
    finance_type = models.CharField(
        "财务类型",
        max_length=128,
        choices=AFTERSALE_FINANCE_TYPE_CHOICES,
        blank=True,
        null=True,
        default=AftersaleFinanceType.AUTO)
    hg_income_cash = models.DecimalField(
        "用户补给汉光的现金额", decimal_places=2, max_digits=12, default=0)
    ## 需求版本v190611 增加 tracking_no, source, user_reason
    # 退货快递单号
    tracking_no = models.CharField("退货快递单号", max_length=64, blank=True, null=True)
    # 售后来源
    source = models.CharField(
        "售后来源",
        max_length=64,
        blank=True,
        null=True,
        choices=AFTERSALE_SOURCE_CHOICES,
        default="")
    # 申请原因
    user_reason = models.CharField("用户申请原因", max_length=512, blank=True, null=True)

    # status变为 待退货 时的时间
    pending_return_time = models.DateTimeField("待退货状态时间", blank=True, null=True, db_index=True)

    # 售后人
    aftersale_user = models.CharField("售后人", max_length=64, blank=True, null=True)

    # 售后人联系方式
    aftersale_phone = models.CharField("售后人联系方式", max_length=64, blank=True, null=True)

    # customer_user_id  (客户id)
    customer_user_id = models.CharField('客户id', max_length=255, blank=True, null=True, db_index=True)

    # customer_member_xx_level (客户会员级别)
    customer_member_xx_level = models.CharField('Customer Member Level', max_length=128, blank=True, null=True)

    # customer_member_number (客户会员号)
    customer_member_number = models.CharField('Customer Member Number', max_length=128, blank=True, null=True)

    # customer_displayname (客户昵称)
    customer_displayname = models.CharField('客户昵称', max_length=15, help_text=u'客户昵称', blank=True, null=True)

    # customer_username (客户手机号)
    customer_username = models.CharField('客户手机号', max_length=15, help_text=u'客户手机号', blank=True, null=True)

    # 取消售后来源
    cancel_source = models.CharField("取消售后来源", max_length=64, blank=True, null=True)

    # 售后类型
    aftersale_type = models.CharField("售后类型", max_length=128, choices=AFTERSALE_TYPE_CHOICES, blank=True, null=True, default=AfterSaleType.NORMAL)

    # 订单类型
    order_type = models.CharField('订单类型', max_length=64, blank=True, null=True)

    # 支付方法（once 一次支付/twice两次支付）
    pay_method = models.CharField("支付方法", max_length=24,choices=PayMethod.PAY_METHOD_CHOICES, blank=True, null=True, default=PayMethod.ONCE)

    class Meta:
        app_label = APP_LABEL
        verbose_name = "Order After Sale"
        verbose_name_plural = "Order After Sale"

    @cached_property
    def coupons_to_charge(self):
        '''系统要扣除用户的优惠券'''
        if not self.id:
            return None
        return AfsCouponToCharge.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_coupons_to_charge(cls, iterable):
        batch_map = defaultdict(list)
        qs = AfsCouponToCharge.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def coupons_to_return(self):
        '''系统要返还用户的优惠券'''
        if not self.id:
            return None
        return AfsCouponToReturn.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_coupons_to_return(cls, iterable):
        batch_map = defaultdict(list)
        qs = AfsCouponToReturn.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @property
    def finance_approver(self):
        if not self.finance_approver_id:
            return None
        return get_object_or_None(get_user_model(), id=self.finance_approver_id)

    @cached_property
    def creator(self):
        if not self.creator_id:
            return None
        return get_object_or_None(get_user_model(), id=self.creator_id)

    @classmethod
    def _batch_creator(cls, iterable):
        qs = get_user_model().objects.filter(id__in=[_.creator_id for _ in iterable if _])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.creator_id) for _ in iterable}

    def __str__(self):
        return 'orderid_{0}--afsid_{1}'.format(self.order_id, self.id)

    @cached_property
    def order(self):
        return get_object_or_None(Order, id=self.order_id)

    @classmethod
    def _batch_order(cls, iterable):
        qs = Order.objects.filter(id__in=[_.order_id for _ in iterable if _])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.order_id) for _ in iterable}

    @cached_property
    def line_after_sales(self):
        return AfsLine.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_line_after_sales(cls, iterable):
        batch_map = defaultdict(list)
        qs = AfsLine.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def aftersale_notes(self):
        return AfsNote.objects.filter(aftersale_id=self.id)

    @classmethod
    def _batch_aftersale_notes(cls, iterable=None):
        batch_map = defaultdict(list)
        qs = AfsNote.objects.filter(aftersale_id__in=[_.id for _ in iterable])
        for q in qs:
            for i in iterable:
                if q.aftersale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def sum_return_amount_map(self):
        points_map = AfsLine.objects.filter(aftersale_id=self.id).values(
            'points_to_charge')\
            .aggregate(
                points_to_charge=Sum('points_to_charge')
            )
        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = AfslinePaymentReturn.objects.filter(
            aftersale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_return": 0,
            "cash_type_amount": 0,
            "a_coupon_to_return": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_return"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_return"] += p["amount"]
        points_map.update(payment_map)
        return points_map

    @property
    def total_refund_cash_amount(self):
        amount = self.total_cash_amount + self.postage - self.hg_income_cash
        if amount < 0:
            amount = 0
        return amount

    @property
    def total_cash_amount(self):
        # import pdb; pdb.set_trace()
        amount = self.sum_return_amount_map.get('cash_type_amount')
        if not amount:
            amount = 0
        return amount

    @property
    def total_cash_amount_with_postage(self):
        # import pdb; pdb.set_trace()
        cash_type_amount = self.sum_return_amount_map.get('cash_type_amount')
        if not cash_type_amount:
            cash_type_amount = Decimal(0)
        else:
            cash_type_amount = Decimal(cash_type_amount)
        postage = self.postage
        if not postage:
            postage = Decimal(0)
        amount = cash_type_amount + postage
        return amount

    @property
    def total_points_to_charge(self):
        amount = self.sum_return_amount_map.get('points_to_charge')
        if not amount:
            amount = 0
        return amount

    @property
    def total_c_coupon_to_return(self):
        amount = self.sum_return_amount_map.get('c_coupon_to_return')
        if not amount:
            amount = 0
        return amount

    @property
    def total_a_coupon_to_return(self):
        amount = self.sum_return_amount_map.get('a_coupon_to_return')
        if not amount:
            amount = 0
        return amount

    @property
    def total_a_coupon_to_charge(self):
        amount = self.sum_charge_amount_map.get('a_coupon_to_charge')
        if not amount:
            amount = 0
        return amount

    @cached_property
    def sum_charge_amount_map(self):
        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = AfslinePaymentCharge.objects.filter(
            aftersale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_charge": 0,
            "cash_type_amount": 0,
            "a_coupon_to_charge": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_charge"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_charge"] += p["amount"]
        return payment_map

    @property
    def payment_type(self):
        payments = OrderPayment.objects.filter(order_id=self.order_id)
        payment_types = [_.payment_type for _ in payments]
        _payment_type = ""
        if PayType.WECHAT in payment_types:
            _payment_type = PayType.WECHAT
        elif PayType.ALIPAY in payment_types:
            _payment_type = PayType.ALIPAY
        return _payment_type

    @property
    def return_remaining_time(self):
        if self.pending_return_time:
            now = datetime.datetime.now()
            future = self.pending_return_time + datetime.timedelta(days=7)
            if future >= now:
                remaining = future - now
                return "{}天{}小时".format(remaining.days, int(remaining.seconds/(60*60)))
            return None
        return None

    @cached_property
    def hg_income_details(self):
        return AfsHgIncomeDetail.objects.filter(aftersale_id=self.id,deleted=False)

    @property
    def status_for_c(self):
        '''
        C端待退货显示优先级：
            1.待外仓确认退货
            2.待客服退货
            3.待客人退货
        '''
        status = self.status
        status_for_c = status
        if status == AftersaleStatus.PENDING_RETURN:

            status_for_c = AftersaleStatus.PENDING_RETURN_0  # 默认待客服退货
            afs_lines = self.line_after_sales
            if_exist_WAIT_OUTSTORAGE = False
            if_exist_WAIT_CUSTOMER = False
            if_exist_WAIT_CUSSERVICE = False
            for afs_line in afs_lines:
                distribute_status = afs_line.distribute_status
                if_returned = afs_line.if_returned
                if if_returned:
                    continue

                if distribute_status in [DistributeStatus.OUTSTORAGE_WAIT_PACKAGE]:
                    if_exist_WAIT_OUTSTORAGE = True
                if distribute_status in [DistributeStatus.PACKAGED,
                                            DistributeStatus.CUS_CONFIRM,
                                            DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                                            DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                                            DistributeStatus.OUTSTORAGE_PACKAGED]:
                    if_exist_WAIT_CUSTOMER = True
                if distribute_status in [DistributeStatus.CUSSERVICE_PICKED_UP, DistributeStatus.SERVICE_DESK, DistributeStatus.SERVICE_STORE, DistributeStatus.SERVICE_STOP]:
                    if_exist_WAIT_CUSSERVICE = True

            if if_exist_WAIT_OUTSTORAGE:
                status_for_c = AftersaleStatus.PENDING_RETURN_2  # 待外仓退货
            elif if_exist_WAIT_CUSSERVICE:
                status_for_c = AftersaleStatus.PENDING_RETURN_0  # 默认待客服退货
            elif if_exist_WAIT_CUSTOMER:
                status_for_c = AftersaleStatus.PENDING_RETURN_1  # 待客户退货

        return status_for_c

    @property
    def if_need_shipping_number_dict(self):
        '''
        是否需要客户回填运单号，如果是，返回{
            "if_need_shipping_number": True,
            "shipping_number_list": []
        }
        如果否，返回{
            "if_need_shipping_number": False,
            "shipping_number_list": []
        }
        '''
        status = self.status
        # status_for_c = status
        if_need_shipping_number = False
        shipping_number_list = []
        if status == AftersaleStatus.PENDING_RETURN:

            # status_for_c = AftersaleStatus.PENDING_RETURN_0  # 默认待客服退货
            afs_lines = self.line_after_sales
            # if_exist_WAIT_OUTSTORAGE = False
            # if_exist_WAIT_CUSTOMER = False
            # if_exist_WAIT_CUSSERVICE = False
            for afs_line in afs_lines:
                distribute_status = afs_line.distribute_status
                if_returned = afs_line.if_returned
                # if if_returned:
                #     continue
                customer_express_code = afs_line.customer_express_code
                afs_line_customer_express_name = afs_line.customer_express_name or ""
                customer_express_name = ShippingPartnerCodes_DICT.get(customer_express_code, afs_line_customer_express_name)
                customer_shipping_number = afs_line.customer_shipping_number

                if distribute_status in [DistributeStatus.PACKAGED, 
                                        DistributeStatus.CUS_CONFIRM,
                                        DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                                        DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE,
                                        DistributeStatus.OUTSTORAGE_PACKAGED]:
                    if not customer_shipping_number and not if_returned:
                        if_need_shipping_number = True
                    elif not customer_shipping_number and if_returned:
                        continue
                    else:
                        shipping_number_list.append(customer_express_name + customer_shipping_number)

        result = {
            "if_need_shipping_number": if_need_shipping_number,
            "shipping_number_list": list(set(shipping_number_list)) if shipping_number_list else shipping_number_list
        }

        return result


class AfsLine(BaseModelTimeAndDeleted):
    '''
    AfterSale 和 Line 的多对多关系表
    '''
    aftersale_id = models.PositiveIntegerField(
        'AfterSale ID', blank=True, null=True, db_index=True)
    line_id = models.PositiveIntegerField(
        'Line ID', blank=True, null=True, db_index=True)
    # quantity值只能是1，为了兼容老代码，保留此字段。
    quantity = models.PositiveIntegerField('SKU退货数量', default=1)
    # 现金类退款金额, 包括支付宝，微信，银行卡，现金
    # 所有数量一共的退款
    # To be deleted by Jessica 2019-07-15 because of 售后单重构
    # cash_type_amount = models.DecimalField(
    #     "现金类金额", decimal_places=2, max_digits=12, default=0)
    # 系统要扣用户的积分（当年发给用户的，现在用户要补缴）
    points_to_charge = models.PositiveIntegerField(
        '系统需要扣除用户的积分', default=0, blank=True, null=True)
    # 系统要还用户的C券（当年被用户用掉的，现在退货了要返还）--历史备注，暂时保留
    '''
    售后单数据库结构重构 说明 By Jessica 2019-07-15:
    points_to_charge和points_to_return两个字段本来应该是成对的，前者表示“扣除客户积分”，后者表示“退还客户积分”。
    由于历史原因，points_to_return在使用中，变成了“退还客户C券”的意义。
    因此在本次数据库调整中，points_to_return需要改回为“退还客户积分”的意义。
    改回前，需要把points_to_return“退还客户C券”的数据挪至sparrow_order_LineAfterSalePaymentReturn表中。
    '''
    points_to_return = models.PositiveIntegerField(
        '系统需要返还用户的积分', default=0, blank=True, null=True)
    # 系统要扣用户的A券（当年用户用掉的，现在用户要补缴）
    # To be deleted by Jessica 2019-07-15 because of 售后单重构
    # a_coupon_to_charge = models.PositiveIntegerField(
    #     '系统需要扣除用户的A券', default=0, blank=True, null=True)
    # 系统要还用户的A券（当年被用户用掉的，现在退货了要返还）
    # To be deleted by Jessica 2019-07-15 because of 售后单重构
    # a_coupon_to_return = models.PositiveIntegerField(
    #     '系统需要返还用户的A券', default=0, blank=True, null=True)
    # 店内系统需要用的流水号——默认先放0，然后传店内系统的时候必须生成flow_id，第一个会从1开始
    flow_id = models.PositiveIntegerField('流水号', default=0, blank=True, null=True)
    # 为了原值活动，必须存下来退了多少当时汉光承担的优惠
    # 这个数据在一期是根据其他退的金额动态算出来的。
    # 存下来的原因是对同一个订单可能有多个退单，而新退单必须知道以前已经退了多少汉光优惠
    discount_hg = models.DecimalField(
        "汉光优惠金额", default=0, decimal_places=2, max_digits=12, blank=True, null=True)

    # 产生售后对应的订单ID，新增冗余字段 by Jessica 2019-07-15
    order_id = models.PositiveIntegerField('Order Id', blank=True, null=True, db_index=True)
    # 中分类，新增冗余字段 by Jessica 2019-07-15
    offer = models.CharField("中分类", max_length=2, default="0")

    # ---------------------------------- 新增字段 -----------------------------------

    # distribute_id(新发货单id,新增)
    distribute_id = models.CharField('新发货单 ID', max_length=100, blank=True, null=True)
    # distribute_number(发货单号）
    distribute_number = models.CharField("Distribute Number", max_length=128, blank=True, null=True)
    # distribute_line_id(新发货单行id,新增)
    distribute_line_id = models.CharField('新发货单行 ID', max_length=100, blank=True, null=True, db_index=True)
    # distribute_status(配货单状态：初始态、已打印、导购已取货、客服已取货、已发货等等)
    distribute_status = models.CharField('配货单状态', max_length=128, blank=True, null=True, choices=DistributeStatus.DISTRIBUTE_STATUS_CHOICES, db_index=True)
    # brand_id(品牌id)
    brand_id = models.PositiveIntegerField('Brand ID', blank=True, null=True)
    # shop_id(专柜id)
    shop_id = models.PositiveIntegerField('Shop ID', blank=True, null=True)
    # shop_num(专柜号)
    shop_num = models.CharField("Shop number", max_length=128, blank=True)
    # product_id(商品id)
    product_id = models.PositiveIntegerField('Product ID', blank=True, null=True, db_index=True)
    # giftproduct_id(赠品id)
    giftproduct_id = models.PositiveIntegerField('赠品 ID', blank=True, null=True, db_index=True)
    # title(商品名称)
    title = models.CharField("Product title", max_length=255, blank=True, null=True)
    # order_number (订单编码)
    order_number = models.CharField('Order Number', max_length=128, blank=True, null=True)
    # if_returned (是否确收退货,新增)
    if_returned = models.BooleanField("是否确收退货", default=False)
    # return_confirmer (确收人,新增)
    return_confirmer = models.CharField( "确收人", max_length=100, blank=True, null=True, db_index=True)
    # confirm_return_time (确收时间,新增)
    confirm_return_time = models.DateTimeField("确收时间", blank=True, null=True)
    # aftersale_number(售后单号)
    aftersale_number = models.CharField('Aftersale Number', max_length=128, blank=True, null=True)

    main_image = models.ImageField("Main Image", null=True, blank=True, max_length=255)
    shop_sku = models.CharField("Shop SKU", max_length=128, blank=True, null=True)
    shop_name = models.CharField("Shop Name", max_length=128, blank=True, null=True)
    brand_name = models.CharField("Brand Name", max_length=128, blank=True, null=True)
    is_gift = models.BooleanField("是否是赠品", default=False)
    is_fixed_price_product = models.BooleanField("是否为换购", default=False)# 商品条码
    barcode = models.CharField("Product Barcode", max_length=1024, default='0')
    sku_attr = models.CharField("Product SKU Attr", max_length=255, blank=True, null=True)
    # 商品汉光码
    hg_code = models.CharField("Product HG Code", max_length=255, blank=True, null=True)
    # 这个商品的原价（比如吊牌价）（1件的价格）
    original_price = models.DecimalField("Original Price", decimal_places=2, max_digits=12, blank=True, null=True)
    # 这个商品的售价（1件的价格）
    retail_price = models.DecimalField("Retail Price", decimal_places=2, max_digits=12, blank=True, null=True)

    # 客户退货回填的快递公司代码
    customer_express_code = models.CharField('客户退货回填的快递公司代码', max_length=64, blank=True, null=True)
    # 客户退货回填的快递公司代码映射成的快递公司名称, 对接微信退单组件时, 为了兼容在微信那边存在而可能在汉光不存在的快递公司添加的字段
    customer_express_name = models.CharField('客户退货回填的快递公司代码映射成的快递公司名称', max_length=64, blank=True, null=True)
    # 客户退货回填的运单号
    customer_shipping_number = models.CharField('客户退货回填的运单号', max_length=64, blank=True, null=True)
    # 外仓id
    outstorage_id = models.CharField("Outstorage ID", max_length=255, blank=True, null=True, db_index=True)
    # productmain_id 主商品ID
    productmain_id = models.PositiveIntegerField('ProductMain ID', blank=True, null=True, db_index=True)

    # 2021 年 9 月 对接微信退货组件新增字段 return_id
    return_id = models.CharField("微信组件退货ID", max_length=64, blank=True, null=True)


    class Meta:
        # 同一个售后单里不应该创建两个相同发货单行的售后
        # unique_together = ('aftersale_id', 'line_id', 'distribute_line_id')
        app_label = APP_LABEL

    @cached_property
    def line(self):
        return get_object_or_None(Line, id=self.line_id)

    @classmethod
    def _batch_line(cls, iterable):
        qs = Line.objects.filter(id__in=[_.line_id for _ in iterable])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.line_id) for _ in iterable}

    @cached_property
    def line_coupons_to_charge(self):
        return AfslinePaymentCharge.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )

    @classmethod
    def _batch_line_coupons_to_charge(cls, iterable):
        batch_map = defaultdict(list)
        qs = AfslinePaymentCharge.objects.filter(
            line_after_sale_id__in=[_.id for _ in iterable],
            payment_type=PayType.GIFT_COUPON
        )
        for q in qs:
            for i in iterable:
                if q.line_after_sale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @cached_property
    def line_coupons_to_return(self):
        return AfslinePaymentReturn.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )

    @classmethod
    def _batch_line_coupons_to_return(cls, iterable):
        batch_map = defaultdict(list)
        qs = AfslinePaymentReturn.objects.filter(
            line_after_sale_id__in=[_.id for _ in iterable],
            payment_type=PayType.GIFT_COUPON
        )
        for q in qs:
            for i in iterable:
                if q.line_after_sale_id == i.id:
                    batch_map[i].append(q)
        return batch_map

    @property
    def total_line_coupons_to_charge(self):
        line_coupons_to_charge = AfslinePaymentCharge.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )
        amount = line_coupons_to_charge.aggregate(total_amount=Sum('amount')).get('total_amount')
        if not amount:
            return 0
        return amount

    @property
    def total_line_coupons_to_return(self):
        line_coupons_to_return = AfslinePaymentReturn.objects.filter(
            line_after_sale_id=self.id,
            payment_type=PayType.GIFT_COUPON
        )
        amount = line_coupons_to_return.aggregate(total_amount=Sum('amount')).get('total_amount')
        if not amount:
            return 0
        return amount

    @cached_property
    def sum_return_amount_map(self):

        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = AfslinePaymentReturn.objects.filter(
            line_after_sale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_return": 0,
            "cash_type_amount": 0,
            "a_coupon_to_return": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_return"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_return"] += p["amount"]
        return payment_map

    @property
    def cash_type_amount(self):
        return self.sum_return_amount_map.get("cash_type_amount")

    @property
    def c_coupon_to_return(self):
        return self.sum_return_amount_map.get("c_coupon_to_return")

    @property
    def a_coupon_to_return(self):
        return self.sum_return_amount_map.get("a_coupon_to_return")

    @cached_property
    def sum_charge_amount_map(self):

        CASH_TYPE = [PayType.WECHAT, PayType.ALIPAY]
        payment = AfslinePaymentCharge.objects.filter(
            line_after_sale_id=self.id,
            payment_type__in=[*CASH_TYPE, PayType.A_COUPON, PayType.C_COUPON]).values(
                'payment_type'
            ).annotate(
                amount=Sum('amount')
            )
        payment_map = {
            "c_coupon_to_charge": 0,
            "cash_type_amount": 0,
            "a_coupon_to_charge": 0
        }
        for p in payment:
            if p["payment_type"] in CASH_TYPE:
                payment_map["cash_type_amount"] += p["amount"]
            elif p["payment_type"] == PayType.A_COUPON:
                payment_map["a_coupon_to_charge"] += p["amount"]
            elif p["payment_type"] == PayType.C_COUPON:
                payment_map["c_coupon_to_charge"] += p["amount"]
        return payment_map

    @property
    def a_coupon_to_charge(self):
        return self.sum_charge_amount_map.get("a_coupon_to_charge")

    @property
    def shop_income_refund(self):
        '''专柜收入退款共计'''
        amount = Decimal('0.00')
        if not self.discount_hg:
            self.discount_hg = 0
        amount += Decimal(self.cash_type_amount) + Decimal(self.c_coupon_to_return) + Decimal(self.a_coupon_to_return)
        amount += Decimal(self.total_line_coupons_to_return)
        amount += Decimal(self.discount_hg)
        return amount

    @property
    def who_need_to_return(self):
        '''
        需要谁还货，当不需要还货时，返回None
        '''
        if self.quantity == 0:
            return None
        if self.distribute_status in [DistributeStatus.INIT, DistributeStatus.PRINTED, DistributeStatus.GUIDE_PICKED_UP, DistributeStatus.HAITAO_INIT]:
            return None
        elif self.distribute_status in [DistributeStatus.PACKAGED, 
                                            DistributeStatus.CUS_CONFIRM,
                                            DistributeStatus.CUS_CONFIRM_AT_GUIDE,
                                            DistributeStatus.CUS_CONFIRM_AT_CUSSERVICE, 
                                            DistributeStatus.OUTSTORAGE_PACKAGED]:
            return "CUSTOMER"  # 待客服退货
        elif self.distribute_status in [DistributeStatus.OUTSTORAGE_WAIT_PACKAGE]:
            return "OUTSTORAGE"  # 待外仓确认退货
        else:
            return "CUSSERVICE"  # 待客服退货

    @property
    def line_order_promotions(self):
        return LineOrderPromotion.objects.filter(
            line_id=self.line_id
        )


class AfsHgIncomeDetail(BaseModelTimeAndDeleted):
    '''
    售后单汉光其他收入明细，与售后单Aftersale表关系为多对一，即一个售后单可以存在多个AfterSaleHgIncome
    hgincome_type_id目前只有三种'积分、券、快递费',由AfterSaleHgIncomeType维护
    每个售后单的每种hgincome_type_id只能唯一

    '''
    order_id = models.IntegerField('订单ID', blank=True, null=True, db_index=True)
    aftersale_id = models.IntegerField('AFS ID', blank=True, null=True, db_index=True)
    hgincome_type_id = models.IntegerField('hgincome Type ID', blank=True, null=True, db_index=True)
    amount = models.DecimalField("Amount", decimal_places=2, max_digits=12, blank=True, null=True, default=0)

    class Meta:
        app_label = APP_LABEL


class AfsPaymentBase(BaseModelTimeAndDeleted):
    '''
    Added by Jessica 2019-07-15
    订单对应的售后支付处理
    '''
    CouponSourceChoices = (
        (CouponSource.ONLINE, '线上'),
        (CouponSource.IN_STORE, '店内')
    )
    # 售后单ID
    aftersale_id = models.PositiveIntegerField('Aftersale Id', blank=True, null=True, db_index=True)
    # 支付类型
    payment_type = models.CharField(
        "Payment type", max_length=10,
        choices=PayType.PAYMENT_TYPE_CHOICES,
        default=PayType.TO_PAY
    )
    # 数额
    amount = models.DecimalField("Amount",decimal_places=2, max_digits=12)
    # 店内系统的话，code存在coupon_id里
    coupon_id = models.CharField(
        'Coupon ID', max_length=50, blank=True, null=True, db_index=True)
    # 店内系统的话，listid存在coupon_number里
    coupon_number = models.CharField(
        'Coupon Number', max_length=64, blank=True, null=True, db_index=True)
    coupon_source = models.CharField(
        '来源', max_length=64, blank=True, null=True,
        choices=CouponSourceChoices
    )
    # 产生售后对应的订单ID
    order_id = models.PositiveIntegerField('Order Id', blank=True, null=True, db_index=True)

    class Meta:
        abstract = True
        app_label = APP_LABEL


class AfsPaymentCharge(AfsPaymentBase):
    '''
    订单对应的售后支付处理: 从客户扣除，它是对AfslinePaymentCharge的汇总
    '''
    payment_num = models.CharField('支付号', max_length=50, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL


class AfsPaymentReturn(AfsPaymentBase):
    '''
    订单对应的售后支付处理：退还给客户，它是对AfslinePaymentReturn的汇总
    '''
    payment_num = models.CharField('支付号', max_length=50, blank=True, null=True)
    # pay_step_type 支付阶段(all全款/deposit定金/tail尾款)
    pay_step_type = models.CharField("支付阶段", max_length=24, choices=PayStepType.PAY_STEP_TYPE_CHOICES, default=PayStepType.ONCE, db_index=True)
    # aftersale_number 退单编号
    aftersale_number = models.CharField('退单编号', max_length=64, blank=True, null=True)
    # aftersale_number_refund 退单子退款编号
    aftersale_number_refund = models.CharField('退单子退款编号', max_length=64, blank=True, null=True)
    # aftersale_number_refund_status 退单子退款状态(init初始/doing进行中/done已完成)
    aftersale_number_refund_status = models.CharField("退单子退款状态", max_length=16, blank=True, null=True, choices=Aftersale_Number_Refund_Status.AFTERSALE_NUMBER_REFUND_STATUS_CHOICES, default=Aftersale_Number_Refund_Status.INIT, db_index=True)

    class Meta:
        app_label = APP_LABEL


class AfslinePaymentBase(AfsPaymentBase):
    '''
    订单Line对应的售后支付处理
    '''
    # 售后Line ID
    line_after_sale_id = models.PositiveIntegerField('AfsLine Id', blank=True, null=True, db_index=True)
    # 产生售后对应的订单Line ID
    line_id = models.PositiveIntegerField('Line Id', blank=True, null=True, db_index=True)

    class Meta:
        abstract = True
        app_label = APP_LABEL


class AfslinePaymentCharge(AfslinePaymentBase):
    '''
    订单Line对应的售后支付处理: 从客户扣除
    '''
    class Meta:
        app_label = 'sparrow_aftersale'


class AfslinePaymentReturn(AfslinePaymentBase):
    '''
    订单Line对应的售后支付处理：退还给客户
    '''
    # pay_step_type 支付阶段(all全款/deposit定金/tail尾款)
    pay_step_type = models.CharField("支付阶段", max_length=24, choices=PayStepType.PAY_STEP_TYPE_CHOICES, default=PayStepType.ONCE, db_index=True)

    class Meta:
        app_label = APP_LABEL


class AfsCouponBase(BaseModelTimeAndDeleted):
    CouponSourceChoices = (
        (CouponSource.ONLINE, '线上'),
        (CouponSource.IN_STORE, '店内')
    )
    aftersale_id = models.PositiveIntegerField('AfterSale ID', blank=True, null=True, db_index=True)
    # 店内系统的话，code存在coupon_id里
    coupon_id = models.CharField('Coupon ID', max_length=50, blank=True, null=True, db_index=True)
    # 店内系统的话，listid存在coupon_number里
    coupon_number = models.CharField('Coupon Number', max_length=64, blank=True, null=True, db_index=True)
    coupon_source = models.CharField('来源', max_length=64, default=CouponSource.IN_STORE, choices=CouponSourceChoices)
    # 产生售后对应的订单ID，新增冗余字段 by Jessica 2019-07-15
    order_id = models.PositiveIntegerField('Order Id', blank=True, null=True, db_index=True)

    class Meta:
        abstract = True
        app_label = APP_LABEL

    @property
    def coupon(self):
        return get_object_or_None(Coupon, id=self.coupon_id)


class AfsCouponToCharge(AfsCouponBase):
    '''需要用户补缴的coupon，系统要从用户那儿收回的coupon 默认数量是1'''

    class Meta:
        app_label = 'sparrow_aftersale'
        app_label = APP_LABEL


class AfsCouponToReturn(AfsCouponBase):
    '''系统退给用户的coupon 数量默认都是1！'''

    class Meta:
        app_label = APP_LABEL


class AfsNote(BaseModelTimeAndDeleted):
    '''
    售后单日志
    '''
    ACTION_CHOICES = (
        (AftersaleActions.CREATE, '创建售后单'),
        (AftersaleActions.REMOVE, '关闭售后单'),
        (AftersaleActions.COMPLETE, '完成售后单'),
        (AftersaleActions.OPERATOR_APPROVE, '客服通过审核'),
        (AftersaleActions.FINANCE_APPROVE_1ST, '财务一审通过'),
        (AftersaleActions.FINANCE_APPROVE, '财务二审通过'),
        (AftersaleActions.FINANCE_REJECT, '财务驳回'),
        (AftersaleActions.INSTORE_REJECT, '店内系统驳回'),
        (AftersaleActions.ALL_APPROVE, '店内系统通过'),
        (AftersaleActions.REFUND_FAIL, '退款失败'),
        (AftersaleActions.PENDING_RETURN, '待退货'),
        (AftersaleActions.PENDING_REFUND, '待退款'),
        # (AftersaleActions.START_REFUND, '开始退款'),
        # (AftersaleActions.REFUND_SUCCEED, '退款成功'),
        (AftersaleActions.CONFIRM_RETURNED, '确认已收到退货'),
        (AftersaleActions.CUSSERVICE_MODIFY_EXPRESS, '客服修改运单信息'),
    )
    user_id = models.CharField(
        "User Id", max_length=100, blank=True, null=True, db_index=True)
    order_id = models.IntegerField('订单ID',
                                   blank=True, null=True, db_index=True)
    aftersale_id = models.IntegerField('AfterSale ID',
                                       blank=True, null=True, db_index=True)
    line_aftersale_id = models.IntegerField('AfsLine ID',
                                            blank=True, null=True, db_index=True)
    action = models.CharField(
        'Action', max_length=128, blank=True, null=True, choices=ACTION_CHOICES, db_index=True)
    message = models.CharField(
        'Message', max_length=2048, blank=True, null=True)

    class Meta:
        app_label = APP_LABEL

    @cached_property
    def user(self):
        if not self.user_id:
            return None
        return get_object_or_None(get_user_model(), id=self.user_id)

    @classmethod
    def _batch_user(cls, iterable):
        qs = get_user_model().objects.filter(id__in=[_.user_id for _ in iterable])
        qs_map = {_.id: _ for _ in qs}
        return {_: qs_map.get(_.user_id) for _ in iterable if qs_map.get(_.user_id)}


class AfsAlipayRefund(models.Model):
    """
    发起过支付宝退款并且返回值为10000的会有记录，作用是查询一些争议退款情况
    """
    aftersale_id = models.PositiveIntegerField('AfterSale Id', unique=True)
    order_number = models.CharField('Order ID', max_length=128, blank=True, null=True)
    amount = models.DecimalField("退款金额", decimal_places=2, max_digits=12, default=0.00)
    user_id = models.CharField("User Id",max_length=100, db_index=True)
    trade_no = models.CharField('支付宝交易号', max_length=64, blank=True, null=True)
    buyer_logon_id = models.CharField('用户的登录id', max_length=100, blank=True, null=True)
    buyer_user_id = models.CharField('买家在支付宝的用户id', max_length=28, blank=True, null=True)
    fund_change = models.CharField('本次退款是否发生了资金变化', max_length=2, blank=True, null=True)
    refund_fee = models.CharField('金额', max_length=11, blank=True, null=True)
    out_trade_no = models.CharField('商户订单号', max_length=64, blank=True, null=True)
    out_request_no = models.CharField('支付宝退款请求号', max_length=64, blank=True, null=True)
    gmt_refund_pay = models.CharField('退款支付时间', max_length=32, blank=True, null=True)
    is_success = models.BooleanField('退款是否成功', default=False)
    created_time = models.DateTimeField("Date Created", blank=True, null=True, auto_now_add=True)
    updated_time = models.DateTimeField("Date Updated", blank=True, null=True, auto_now=True)

    class Meta:
        app_label = APP_LABEL


class DeliveryReturn(BaseModelTimeAndDeleted):
    """ 对接微信退货组件新增表 """

    id = models.CharField("id", primary_key=True, max_length=32, default=get_uuid4_hex)
    return_id = models.CharField("return_id", max_length=64)
    out_shop_id = models.CharField("out_shop_id", max_length=64, null=True)  # 申请退单时传给微信那边的业务ID

    delivery_id = models.CharField("微信退单组件返回的快递公司编码", max_length=64, null=True, blank=True)
    delivery_name = models.CharField("微信退单组件返回的快递公司名称", max_length=64, null=True, blank=True)
    express_code = models.CharField("映射到汉光的快递公司编码", max_length=64, null=True, blank=True)
    express_name = models.CharField("映射到汉光的快递公司名称", max_length=20, null=True, blank=True)
    shipping_number = models.CharField("用户借用退单组件回填的运单号", max_length=64, null=True, blank=True)

    source_type = models.CharField("售后类型", max_length=16)
    source_id = models.CharField("source_id", max_length=32)
    source_number = models.CharField("source_number", max_length=32)
    # 用户回填运单号方式   在线预约/自主填写
    status = models.SmallIntegerField("用户回填运单号方式", db_index=True, default=0, blank=True)
    order_status = models.SmallIntegerField("退单的状态", db_index=True, default=0, blank=True)

    # 回寄给汉光的地址
    hg_addr_province = models.CharField("退回给汉光的地址", max_length=512, blank=True)
    hg_addr_city = models.CharField("退回给汉光的地址", max_length=512, blank=True)
    hg_addr_district = models.CharField("退回给汉光的地址", max_length=512, blank=True)
    hg_addr_detail = models.CharField("退回给汉光的地址", max_length=512, blank=True)
    hg_addr_name = models.CharField("退回给汉光的地址", max_length=32, blank=True)
    hg_addr_phone = models.CharField("退回给汉光的地址", max_length=16, blank=True)
    # 兼容 sparrow_distribute_storageconfig 的 outstorage_name 字段
    outstorage_name = models.CharField("退回给汉光的地址", max_length=512, blank=True)
    outstorage_id = models.CharField("outstorage_id", max_length=64, null=True)

    # 客户退单地址
    user_addr_province = models.CharField("客户的地址", max_length=512, blank=True)
    user_addr_city = models.CharField("客户的地址", max_length=512, blank=True)
    user_addr_district = models.CharField("客户的地址", max_length=512, blank=True)
    user_addr_detail = models.CharField("客户的地址", max_length=512, blank=True)
    user_addr_name = models.CharField("客户的地址", max_length=32, blank=True)
    user_addr_phone = models.CharField("客户的地址", max_length=16, blank=True)

    class Meta:
        index_together = ["source_type", "source_id"]
        app_label = APP_LABEL
