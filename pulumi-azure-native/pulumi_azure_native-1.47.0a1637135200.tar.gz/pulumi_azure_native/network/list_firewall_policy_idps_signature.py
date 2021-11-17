# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'ListFirewallPolicyIdpsSignatureResult',
    'AwaitableListFirewallPolicyIdpsSignatureResult',
    'list_firewall_policy_idps_signature',
    'list_firewall_policy_idps_signature_output',
]

@pulumi.output_type
class ListFirewallPolicyIdpsSignatureResult:
    """
    Query result
    """
    def __init__(__self__, matching_records_count=None, signatures=None):
        if matching_records_count and not isinstance(matching_records_count, float):
            raise TypeError("Expected argument 'matching_records_count' to be a float")
        pulumi.set(__self__, "matching_records_count", matching_records_count)
        if signatures and not isinstance(signatures, list):
            raise TypeError("Expected argument 'signatures' to be a list")
        pulumi.set(__self__, "signatures", signatures)

    @property
    @pulumi.getter(name="matchingRecordsCount")
    def matching_records_count(self) -> Optional[float]:
        """
        Number of total records matching the query.
        """
        return pulumi.get(self, "matching_records_count")

    @property
    @pulumi.getter
    def signatures(self) -> Optional[Sequence['outputs.SingleQueryResultResponse']]:
        """
        Array containing the results of the query
        """
        return pulumi.get(self, "signatures")


class AwaitableListFirewallPolicyIdpsSignatureResult(ListFirewallPolicyIdpsSignatureResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListFirewallPolicyIdpsSignatureResult(
            matching_records_count=self.matching_records_count,
            signatures=self.signatures)


def list_firewall_policy_idps_signature(filters: Optional[Sequence[pulumi.InputType['FilterItems']]] = None,
                                        firewall_policy_name: Optional[str] = None,
                                        order_by: Optional[pulumi.InputType['OrderBy']] = None,
                                        resource_group_name: Optional[str] = None,
                                        results_per_page: Optional[int] = None,
                                        search: Optional[str] = None,
                                        skip: Optional[int] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListFirewallPolicyIdpsSignatureResult:
    """
    Query result
    API Version: 2021-05-01.


    :param Sequence[pulumi.InputType['FilterItems']] filters: Contain all filters names and values
    :param str firewall_policy_name: The name of the Firewall Policy.
    :param pulumi.InputType['OrderBy'] order_by: Column to sort response by
    :param str resource_group_name: The name of the resource group.
    :param int results_per_page: The number of the results to return in each page
    :param str search: Search term in all columns
    :param int skip: The number of records matching the filter to skip
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['firewallPolicyName'] = firewall_policy_name
    __args__['orderBy'] = order_by
    __args__['resourceGroupName'] = resource_group_name
    __args__['resultsPerPage'] = results_per_page
    __args__['search'] = search
    __args__['skip'] = skip
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network:listFirewallPolicyIdpsSignature', __args__, opts=opts, typ=ListFirewallPolicyIdpsSignatureResult).value

    return AwaitableListFirewallPolicyIdpsSignatureResult(
        matching_records_count=__ret__.matching_records_count,
        signatures=__ret__.signatures)


@_utilities.lift_output_func(list_firewall_policy_idps_signature)
def list_firewall_policy_idps_signature_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['FilterItems']]]]] = None,
                                               firewall_policy_name: Optional[pulumi.Input[str]] = None,
                                               order_by: Optional[pulumi.Input[Optional[pulumi.InputType['OrderBy']]]] = None,
                                               resource_group_name: Optional[pulumi.Input[str]] = None,
                                               results_per_page: Optional[pulumi.Input[Optional[int]]] = None,
                                               search: Optional[pulumi.Input[Optional[str]]] = None,
                                               skip: Optional[pulumi.Input[Optional[int]]] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListFirewallPolicyIdpsSignatureResult]:
    """
    Query result
    API Version: 2021-05-01.


    :param Sequence[pulumi.InputType['FilterItems']] filters: Contain all filters names and values
    :param str firewall_policy_name: The name of the Firewall Policy.
    :param pulumi.InputType['OrderBy'] order_by: Column to sort response by
    :param str resource_group_name: The name of the resource group.
    :param int results_per_page: The number of the results to return in each page
    :param str search: Search term in all columns
    :param int skip: The number of records matching the filter to skip
    """
    ...
