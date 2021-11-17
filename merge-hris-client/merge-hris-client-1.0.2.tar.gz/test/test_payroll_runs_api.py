"""
    Merge HRIS API

    The unified API for building rich integrations with multiple HR Information System platforms.  # noqa: E501

    The version of the OpenAPI document: 1.0
    Contact: hello@merge.dev
    Generated by: https://openapi-generator.tech
"""


import unittest

import MergeHRISClient
from MergeHRISClient.api.payroll_runs_api import PayrollRunsApi  # noqa: E501


class TestPayrollRunsApi(unittest.TestCase):
    """PayrollRunsApi unit test stubs"""

    def setUp(self):
        self.api = PayrollRunsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_payroll_runs_list(self):
        """Test case for payroll_runs_list

        """
        pass

    def test_payroll_runs_retrieve(self):
        """Test case for payroll_runs_retrieve

        """
        pass


if __name__ == '__main__':
    unittest.main()
