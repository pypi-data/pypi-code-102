# coding: utf-8

"""
    Merge HRIS API

    The unified API for building rich integrations with multiple HR Information System platforms.  # noqa: E501

    The version of the OpenAPI document: 1.0
    Contact: hello@merge.dev
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from MergeHRISClient.configuration import Configuration


class PatchedEmployeePayrollRun(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'remote_id': 'str',
        'employee': 'str',
        'payroll_run': 'str',
        'gross_pay': 'float',
        'net_pay': 'float',
        'start_date': 'datetime',
        'end_date': 'datetime',
        'check_date': 'datetime',
        'earnings': 'list[Earning]',
        'deductions': 'list[Deduction]',
        'taxes': 'list[Tax]'
    }

    attribute_map = {
        'id': 'id',
        'remote_id': 'remote_id',
        'employee': 'employee',
        'payroll_run': 'payroll_run',
        'gross_pay': 'gross_pay',
        'net_pay': 'net_pay',
        'start_date': 'start_date',
        'end_date': 'end_date',
        'check_date': 'check_date',
        'earnings': 'earnings',
        'deductions': 'deductions',
        'taxes': 'taxes'
    }

    def __init__(self, id=None, remote_id=None, employee=None, payroll_run=None, gross_pay=None, net_pay=None, start_date=None, end_date=None, check_date=None, earnings=None, deductions=None, taxes=None, local_vars_configuration=None):  # noqa: E501
        """PatchedEmployeePayrollRun - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._remote_id = None
        self._employee = None
        self._payroll_run = None
        self._gross_pay = None
        self._net_pay = None
        self._start_date = None
        self._end_date = None
        self._check_date = None
        self._earnings = None
        self._deductions = None
        self._taxes = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.remote_id = remote_id
        self.employee = employee
        self.payroll_run = payroll_run
        self.gross_pay = gross_pay
        self.net_pay = net_pay
        self.start_date = start_date
        self.end_date = end_date
        self.check_date = check_date
        if earnings is not None:
            self.earnings = earnings
        if deductions is not None:
            self.deductions = deductions
        if taxes is not None:
            self.taxes = taxes

    @property
    def id(self):
        """Gets the id of this PatchedEmployeePayrollRun.  # noqa: E501


        :return: The id of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PatchedEmployeePayrollRun.


        :param id: The id of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def remote_id(self):
        """Gets the remote_id of this PatchedEmployeePayrollRun.  # noqa: E501

        The third-party API ID of the matching object.  # noqa: E501

        :return: The remote_id of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: str
        """
        return self._remote_id

    @remote_id.setter
    def remote_id(self, remote_id):
        """Sets the remote_id of this PatchedEmployeePayrollRun.

        The third-party API ID of the matching object.  # noqa: E501

        :param remote_id: The remote_id of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: str
        """

        self._remote_id = remote_id

    @property
    def employee(self):
        """Gets the employee of this PatchedEmployeePayrollRun.  # noqa: E501

        The employee who's payroll is being run.  # noqa: E501

        :return: The employee of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: str
        """
        return self._employee

    @employee.setter
    def employee(self, employee):
        """Sets the employee of this PatchedEmployeePayrollRun.

        The employee who's payroll is being run.  # noqa: E501

        :param employee: The employee of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: str
        """

        self._employee = employee

    @property
    def payroll_run(self):
        """Gets the payroll_run of this PatchedEmployeePayrollRun.  # noqa: E501

        The payroll being run.  # noqa: E501

        :return: The payroll_run of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: str
        """
        return self._payroll_run

    @payroll_run.setter
    def payroll_run(self, payroll_run):
        """Sets the payroll_run of this PatchedEmployeePayrollRun.

        The payroll being run.  # noqa: E501

        :param payroll_run: The payroll_run of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: str
        """

        self._payroll_run = payroll_run

    @property
    def gross_pay(self):
        """Gets the gross_pay of this PatchedEmployeePayrollRun.  # noqa: E501

        The gross pay from the run.  # noqa: E501

        :return: The gross_pay of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: float
        """
        return self._gross_pay

    @gross_pay.setter
    def gross_pay(self, gross_pay):
        """Sets the gross_pay of this PatchedEmployeePayrollRun.

        The gross pay from the run.  # noqa: E501

        :param gross_pay: The gross_pay of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: float
        """

        self._gross_pay = gross_pay

    @property
    def net_pay(self):
        """Gets the net_pay of this PatchedEmployeePayrollRun.  # noqa: E501

        The net pay from the run.  # noqa: E501

        :return: The net_pay of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: float
        """
        return self._net_pay

    @net_pay.setter
    def net_pay(self, net_pay):
        """Sets the net_pay of this PatchedEmployeePayrollRun.

        The net pay from the run.  # noqa: E501

        :param net_pay: The net_pay of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: float
        """

        self._net_pay = net_pay

    @property
    def start_date(self):
        """Gets the start_date of this PatchedEmployeePayrollRun.  # noqa: E501

        The day and time the payroll run started.  # noqa: E501

        :return: The start_date of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this PatchedEmployeePayrollRun.

        The day and time the payroll run started.  # noqa: E501

        :param start_date: The start_date of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: datetime
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """Gets the end_date of this PatchedEmployeePayrollRun.  # noqa: E501

        The day and time the payroll run ended.  # noqa: E501

        :return: The end_date of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """Sets the end_date of this PatchedEmployeePayrollRun.

        The day and time the payroll run ended.  # noqa: E501

        :param end_date: The end_date of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: datetime
        """

        self._end_date = end_date

    @property
    def check_date(self):
        """Gets the check_date of this PatchedEmployeePayrollRun.  # noqa: E501

        The day and time the payroll run was checked.  # noqa: E501

        :return: The check_date of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: datetime
        """
        return self._check_date

    @check_date.setter
    def check_date(self, check_date):
        """Sets the check_date of this PatchedEmployeePayrollRun.

        The day and time the payroll run was checked.  # noqa: E501

        :param check_date: The check_date of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: datetime
        """

        self._check_date = check_date

    @property
    def earnings(self):
        """Gets the earnings of this PatchedEmployeePayrollRun.  # noqa: E501


        :return: The earnings of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: list[Earning]
        """
        return self._earnings

    @earnings.setter
    def earnings(self, earnings):
        """Sets the earnings of this PatchedEmployeePayrollRun.


        :param earnings: The earnings of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: list[Earning]
        """

        self._earnings = earnings

    @property
    def deductions(self):
        """Gets the deductions of this PatchedEmployeePayrollRun.  # noqa: E501


        :return: The deductions of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: list[Deduction]
        """
        return self._deductions

    @deductions.setter
    def deductions(self, deductions):
        """Sets the deductions of this PatchedEmployeePayrollRun.


        :param deductions: The deductions of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: list[Deduction]
        """

        self._deductions = deductions

    @property
    def taxes(self):
        """Gets the taxes of this PatchedEmployeePayrollRun.  # noqa: E501


        :return: The taxes of this PatchedEmployeePayrollRun.  # noqa: E501
        :rtype: list[Tax]
        """
        return self._taxes

    @taxes.setter
    def taxes(self, taxes):
        """Sets the taxes of this PatchedEmployeePayrollRun.


        :param taxes: The taxes of this PatchedEmployeePayrollRun.  # noqa: E501
        :type: list[Tax]
        """

        self._taxes = taxes

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PatchedEmployeePayrollRun):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatchedEmployeePayrollRun):
            return True

        return self.to_dict() != other.to_dict()
