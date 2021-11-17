# coding: utf-8

"""
    Aliro Q.Network

    This is an api for the Aliro Q.Network  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: nick@aliroquantum.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import aliro_quantum_networking
from aliro_quantum_networking.models.node import Node  # noqa: E501
from aliro_quantum_networking.rest import ApiException

class TestNode(unittest.TestCase):
    """Node unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Node
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = aliro_quantum_networking.models.node.Node()  # noqa: E501
        if include_optional :
            return Node(
                measurement_error_probability = 0, 
                memories = [
                    null
                    ], 
                name = '0', 
                operation_errors = {
                    'key' : aliro_quantum_networking.models.node_operation_errors.Node_operationErrors(
                        error_models = [
                            aliro_quantum_networking.models.error_model.ErrorModel(
                                error_model_name = 'bitflip', 
                                probability = 0, )
                            ], 
                        gate_name = 'CNOT', )
                    }
            )
        else :
            return Node(
                memories = [
                    null
                    ],
                name = '0',
        )

    def testNode(self):
        """Test Node"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
