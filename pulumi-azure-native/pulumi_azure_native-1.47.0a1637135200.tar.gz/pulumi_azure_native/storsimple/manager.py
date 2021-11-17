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

__all__ = ['ManagerArgs', 'Manager']

@pulumi.input_type
class ManagerArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 cis_intrinsic_settings: Optional[pulumi.Input['ManagerIntrinsicSettingsArgs']] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 manager_name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['ManagerSkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Manager resource.
        :param pulumi.Input[str] resource_group_name: The resource group name
        :param pulumi.Input['ManagerIntrinsicSettingsArgs'] cis_intrinsic_settings: Represents the type of StorSimple Manager.
        :param pulumi.Input[str] etag: The etag of the manager.
        :param pulumi.Input[str] location: The geo location of the resource.
        :param pulumi.Input[str] manager_name: The manager name
        :param pulumi.Input[str] provisioning_state: Specifies the state of the resource as it is getting provisioned. Value of "Succeeded" means the Manager was successfully created.
        :param pulumi.Input['ManagerSkuArgs'] sku: Specifies the Sku.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags attached to the resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if cis_intrinsic_settings is not None:
            pulumi.set(__self__, "cis_intrinsic_settings", cis_intrinsic_settings)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if manager_name is not None:
            pulumi.set(__self__, "manager_name", manager_name)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="cisIntrinsicSettings")
    def cis_intrinsic_settings(self) -> Optional[pulumi.Input['ManagerIntrinsicSettingsArgs']]:
        """
        Represents the type of StorSimple Manager.
        """
        return pulumi.get(self, "cis_intrinsic_settings")

    @cis_intrinsic_settings.setter
    def cis_intrinsic_settings(self, value: Optional[pulumi.Input['ManagerIntrinsicSettingsArgs']]):
        pulumi.set(self, "cis_intrinsic_settings", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        The etag of the manager.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo location of the resource.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="managerName")
    def manager_name(self) -> Optional[pulumi.Input[str]]:
        """
        The manager name
        """
        return pulumi.get(self, "manager_name")

    @manager_name.setter
    def manager_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "manager_name", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the state of the resource as it is getting provisioned. Value of "Succeeded" means the Manager was successfully created.
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['ManagerSkuArgs']]:
        """
        Specifies the Sku.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ManagerSkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags attached to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class Manager(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cis_intrinsic_settings: Optional[pulumi.Input[pulumi.InputType['ManagerIntrinsicSettingsArgs']]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 manager_name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ManagerSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The StorSimple Manager.
        API Version: 2017-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ManagerIntrinsicSettingsArgs']] cis_intrinsic_settings: Represents the type of StorSimple Manager.
        :param pulumi.Input[str] etag: The etag of the manager.
        :param pulumi.Input[str] location: The geo location of the resource.
        :param pulumi.Input[str] manager_name: The manager name
        :param pulumi.Input[str] provisioning_state: Specifies the state of the resource as it is getting provisioned. Value of "Succeeded" means the Manager was successfully created.
        :param pulumi.Input[str] resource_group_name: The resource group name
        :param pulumi.Input[pulumi.InputType['ManagerSkuArgs']] sku: Specifies the Sku.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags attached to the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The StorSimple Manager.
        API Version: 2017-06-01.

        :param str resource_name: The name of the resource.
        :param ManagerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cis_intrinsic_settings: Optional[pulumi.Input[pulumi.InputType['ManagerIntrinsicSettingsArgs']]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 manager_name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ManagerSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = ManagerArgs.__new__(ManagerArgs)

            __props__.__dict__["cis_intrinsic_settings"] = cis_intrinsic_settings
            __props__.__dict__["etag"] = etag
            __props__.__dict__["location"] = location
            __props__.__dict__["manager_name"] = manager_name
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:storsimple/v20161001:Manager"), pulumi.Alias(type_="azure-native:storsimple/v20170601:Manager")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Manager, __self__).__init__(
            'azure-native:storsimple:Manager',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Manager':
        """
        Get an existing Manager resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ManagerArgs.__new__(ManagerArgs)

        __props__.__dict__["cis_intrinsic_settings"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Manager(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cisIntrinsicSettings")
    def cis_intrinsic_settings(self) -> pulumi.Output[Optional['outputs.ManagerIntrinsicSettingsResponse']]:
        """
        Represents the type of StorSimple Manager.
        """
        return pulumi.get(self, "cis_intrinsic_settings")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        The etag of the manager.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the state of the resource as it is getting provisioned. Value of "Succeeded" means the Manager was successfully created.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ManagerSkuResponse']]:
        """
        Specifies the Sku.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags attached to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

