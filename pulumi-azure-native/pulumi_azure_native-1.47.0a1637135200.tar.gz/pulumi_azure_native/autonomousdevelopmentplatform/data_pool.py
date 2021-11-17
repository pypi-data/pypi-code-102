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

__all__ = ['DataPoolArgs', 'DataPool']

@pulumi.input_type
class DataPoolArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 locations: pulumi.Input[Sequence[pulumi.Input['DataPoolLocationArgs']]],
                 resource_group_name: pulumi.Input[str],
                 data_pool_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DataPool resource.
        :param pulumi.Input[str] account_name: The name of the ADP account
        :param pulumi.Input[Sequence[pulumi.Input['DataPoolLocationArgs']]] locations: Gets or sets the collection of locations where Data Pool resources should be created
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] data_pool_name: The name of the Data Pool
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "locations", locations)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if data_pool_name is not None:
            pulumi.set(__self__, "data_pool_name", data_pool_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the ADP account
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def locations(self) -> pulumi.Input[Sequence[pulumi.Input['DataPoolLocationArgs']]]:
        """
        Gets or sets the collection of locations where Data Pool resources should be created
        """
        return pulumi.get(self, "locations")

    @locations.setter
    def locations(self, value: pulumi.Input[Sequence[pulumi.Input['DataPoolLocationArgs']]]):
        pulumi.set(self, "locations", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="dataPoolName")
    def data_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Data Pool
        """
        return pulumi.get(self, "data_pool_name")

    @data_pool_name.setter
    def data_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_pool_name", value)


class DataPool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 data_pool_name: Optional[pulumi.Input[str]] = None,
                 locations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataPoolLocationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ADP Data Pool
        API Version: 2021-02-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the ADP account
        :param pulumi.Input[str] data_pool_name: The name of the Data Pool
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataPoolLocationArgs']]]] locations: Gets or sets the collection of locations where Data Pool resources should be created
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataPoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ADP Data Pool
        API Version: 2021-02-01-preview.

        :param str resource_name: The name of the resource.
        :param DataPoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataPoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 data_pool_name: Optional[pulumi.Input[str]] = None,
                 locations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DataPoolLocationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataPoolArgs.__new__(DataPoolArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["data_pool_name"] = data_pool_name
            if locations is None and not opts.urn:
                raise TypeError("Missing required property 'locations'")
            __props__.__dict__["locations"] = locations
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["data_pool_id"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:autonomousdevelopmentplatform/v20200701preview:DataPool"), pulumi.Alias(type_="azure-native:autonomousdevelopmentplatform/v20210201preview:DataPool")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DataPool, __self__).__init__(
            'azure-native:autonomousdevelopmentplatform:DataPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DataPool':
        """
        Get an existing DataPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DataPoolArgs.__new__(DataPoolArgs)

        __props__.__dict__["data_pool_id"] = None
        __props__.__dict__["locations"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return DataPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dataPoolId")
    def data_pool_id(self) -> pulumi.Output[str]:
        """
        The Data Pool's data-plane ID
        """
        return pulumi.get(self, "data_pool_id")

    @property
    @pulumi.getter
    def locations(self) -> pulumi.Output[Sequence['outputs.DataPoolLocationResponse']]:
        """
        Gets or sets the collection of locations where Data Pool resources should be created
        """
        return pulumi.get(self, "locations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Gets the status of the data pool at the time the operation was called
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

