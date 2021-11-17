# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['NetworkFunctionArgs', 'NetworkFunction']

@pulumi.input_type
class NetworkFunctionArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 device: Optional[pulumi.Input['SubResourceArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_application_parameters: Optional[Any] = None,
                 network_function_name: Optional[pulumi.Input[str]] = None,
                 network_function_user_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkFunctionUserConfigurationArgs']]]] = None,
                 sku_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vendor_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NetworkFunction resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input['SubResourceArgs'] device: The reference to the device resource.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param Any managed_application_parameters: The parameters for the managed application.
        :param pulumi.Input[str] network_function_name: Resource name for the network function resource.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkFunctionUserConfigurationArgs']]] network_function_user_configurations: The network function configurations from the user.
        :param pulumi.Input[str] sku_name: The sku name for the network function.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] vendor_name: The vendor name for the network function.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if device is not None:
            pulumi.set(__self__, "device", device)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if managed_application_parameters is not None:
            pulumi.set(__self__, "managed_application_parameters", managed_application_parameters)
        if network_function_name is not None:
            pulumi.set(__self__, "network_function_name", network_function_name)
        if network_function_user_configurations is not None:
            pulumi.set(__self__, "network_function_user_configurations", network_function_user_configurations)
        if sku_name is not None:
            pulumi.set(__self__, "sku_name", sku_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if vendor_name is not None:
            pulumi.set(__self__, "vendor_name", vendor_name)

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
    @pulumi.getter
    def device(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The reference to the device resource.
        """
        return pulumi.get(self, "device")

    @device.setter
    def device(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "device", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="managedApplicationParameters")
    def managed_application_parameters(self) -> Optional[Any]:
        """
        The parameters for the managed application.
        """
        return pulumi.get(self, "managed_application_parameters")

    @managed_application_parameters.setter
    def managed_application_parameters(self, value: Optional[Any]):
        pulumi.set(self, "managed_application_parameters", value)

    @property
    @pulumi.getter(name="networkFunctionName")
    def network_function_name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource name for the network function resource.
        """
        return pulumi.get(self, "network_function_name")

    @network_function_name.setter
    def network_function_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_function_name", value)

    @property
    @pulumi.getter(name="networkFunctionUserConfigurations")
    def network_function_user_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkFunctionUserConfigurationArgs']]]]:
        """
        The network function configurations from the user.
        """
        return pulumi.get(self, "network_function_user_configurations")

    @network_function_user_configurations.setter
    def network_function_user_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkFunctionUserConfigurationArgs']]]]):
        pulumi.set(self, "network_function_user_configurations", value)

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> Optional[pulumi.Input[str]]:
        """
        The sku name for the network function.
        """
        return pulumi.get(self, "sku_name")

    @sku_name.setter
    def sku_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vendorName")
    def vendor_name(self) -> Optional[pulumi.Input[str]]:
        """
        The vendor name for the network function.
        """
        return pulumi.get(self, "vendor_name")

    @vendor_name.setter
    def vendor_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vendor_name", value)


class NetworkFunction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_application_parameters: Optional[Any] = None,
                 network_function_name: Optional[pulumi.Input[str]] = None,
                 network_function_user_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkFunctionUserConfigurationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vendor_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Network function resource response.
        API Version: 2020-01-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] device: The reference to the device resource.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param Any managed_application_parameters: The parameters for the managed application.
        :param pulumi.Input[str] network_function_name: Resource name for the network function resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkFunctionUserConfigurationArgs']]]] network_function_user_configurations: The network function configurations from the user.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] sku_name: The sku name for the network function.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] vendor_name: The vendor name for the network function.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkFunctionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Network function resource response.
        API Version: 2020-01-01-preview.

        :param str resource_name: The name of the resource.
        :param NetworkFunctionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkFunctionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_application_parameters: Optional[Any] = None,
                 network_function_name: Optional[pulumi.Input[str]] = None,
                 network_function_user_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkFunctionUserConfigurationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vendor_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = NetworkFunctionArgs.__new__(NetworkFunctionArgs)

            __props__.__dict__["device"] = device
            __props__.__dict__["etag"] = etag
            __props__.__dict__["location"] = location
            __props__.__dict__["managed_application_parameters"] = managed_application_parameters
            __props__.__dict__["network_function_name"] = network_function_name
            __props__.__dict__["network_function_user_configurations"] = network_function_user_configurations
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku_name"] = sku_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["vendor_name"] = vendor_name
            __props__.__dict__["managed_application"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["service_key"] = None
            __props__.__dict__["sku_type"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["vendor_provisioning_state"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:hybridnetwork/v20200101preview:NetworkFunction"), pulumi.Alias(type_="azure-native:hybridnetwork/v20210501:NetworkFunction")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NetworkFunction, __self__).__init__(
            'azure-native:hybridnetwork:NetworkFunction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NetworkFunction':
        """
        Get an existing NetworkFunction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkFunctionArgs.__new__(NetworkFunctionArgs)

        __props__.__dict__["device"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["managed_application"] = None
        __props__.__dict__["managed_application_parameters"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_function_user_configurations"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["service_key"] = None
        __props__.__dict__["sku_name"] = None
        __props__.__dict__["sku_type"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["vendor_name"] = None
        __props__.__dict__["vendor_provisioning_state"] = None
        return NetworkFunction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def device(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The reference to the device resource.
        """
        return pulumi.get(self, "device")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedApplication")
    def managed_application(self) -> pulumi.Output['outputs.SubResourceResponse']:
        """
        The resource URI of the managed application.
        """
        return pulumi.get(self, "managed_application")

    @property
    @pulumi.getter(name="managedApplicationParameters")
    def managed_application_parameters(self) -> pulumi.Output[Optional[Any]]:
        """
        The parameters for the managed application.
        """
        return pulumi.get(self, "managed_application_parameters")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkFunctionUserConfigurations")
    def network_function_user_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.NetworkFunctionUserConfigurationResponse']]]:
        """
        The network function configurations from the user.
        """
        return pulumi.get(self, "network_function_user_configurations")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the network function resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> pulumi.Output[str]:
        """
        The service key for the network function resource.
        """
        return pulumi.get(self, "service_key")

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> pulumi.Output[Optional[str]]:
        """
        The sku name for the network function.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter(name="skuType")
    def sku_type(self) -> pulumi.Output[str]:
        """
        The sku type for the network function.
        """
        return pulumi.get(self, "sku_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vendorName")
    def vendor_name(self) -> pulumi.Output[Optional[str]]:
        """
        The vendor name for the network function.
        """
        return pulumi.get(self, "vendor_name")

    @property
    @pulumi.getter(name="vendorProvisioningState")
    def vendor_provisioning_state(self) -> pulumi.Output[str]:
        """
        The vendor provisioning state for the network function resource.
        """
        return pulumi.get(self, "vendor_provisioning_state")

