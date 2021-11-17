# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AdvancedThreatProtectionArgs', 'AdvancedThreatProtection']

@pulumi.input_type
class AdvancedThreatProtectionArgs:
    def __init__(__self__, *,
                 resource_id: pulumi.Input[str],
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 setting_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AdvancedThreatProtection resource.
        :param pulumi.Input[str] resource_id: The identifier of the resource.
        :param pulumi.Input[bool] is_enabled: Indicates whether Advanced Threat Protection is enabled.
        :param pulumi.Input[str] setting_name: Advanced Threat Protection setting name.
        """
        pulumi.set(__self__, "resource_id", resource_id)
        if is_enabled is not None:
            pulumi.set(__self__, "is_enabled", is_enabled)
        if setting_name is not None:
            pulumi.set(__self__, "setting_name", setting_name)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Input[str]:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_id", value)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether Advanced Threat Protection is enabled.
        """
        return pulumi.get(self, "is_enabled")

    @is_enabled.setter
    def is_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_enabled", value)

    @property
    @pulumi.getter(name="settingName")
    def setting_name(self) -> Optional[pulumi.Input[str]]:
        """
        Advanced Threat Protection setting name.
        """
        return pulumi.get(self, "setting_name")

    @setting_name.setter
    def setting_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "setting_name", value)


class AdvancedThreatProtection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 setting_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The Advanced Threat Protection resource.
        API Version: 2019-01-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] is_enabled: Indicates whether Advanced Threat Protection is enabled.
        :param pulumi.Input[str] resource_id: The identifier of the resource.
        :param pulumi.Input[str] setting_name: Advanced Threat Protection setting name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AdvancedThreatProtectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Advanced Threat Protection resource.
        API Version: 2019-01-01.

        :param str resource_name: The name of the resource.
        :param AdvancedThreatProtectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AdvancedThreatProtectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 setting_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = AdvancedThreatProtectionArgs.__new__(AdvancedThreatProtectionArgs)

            __props__.__dict__["is_enabled"] = is_enabled
            if resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'resource_id'")
            __props__.__dict__["resource_id"] = resource_id
            __props__.__dict__["setting_name"] = setting_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:security/v20170801preview:AdvancedThreatProtection"), pulumi.Alias(type_="azure-native:security/v20190101:AdvancedThreatProtection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AdvancedThreatProtection, __self__).__init__(
            'azure-native:security:AdvancedThreatProtection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AdvancedThreatProtection':
        """
        Get an existing AdvancedThreatProtection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AdvancedThreatProtectionArgs.__new__(AdvancedThreatProtectionArgs)

        __props__.__dict__["is_enabled"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return AdvancedThreatProtection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether Advanced Threat Protection is enabled.
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

