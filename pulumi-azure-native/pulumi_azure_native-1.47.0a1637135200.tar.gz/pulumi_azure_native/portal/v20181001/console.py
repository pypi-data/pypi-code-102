# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['ConsoleArgs', 'Console']

@pulumi.input_type
class ConsoleArgs:
    def __init__(__self__, *,
                 properties: pulumi.Input['ConsoleCreatePropertiesArgs'],
                 console_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Console resource.
        :param pulumi.Input['ConsoleCreatePropertiesArgs'] properties: Cloud shell properties for creating a console.
        :param pulumi.Input[str] console_name: The name of the console
        """
        pulumi.set(__self__, "properties", properties)
        if console_name is not None:
            pulumi.set(__self__, "console_name", console_name)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['ConsoleCreatePropertiesArgs']:
        """
        Cloud shell properties for creating a console.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: pulumi.Input['ConsoleCreatePropertiesArgs']):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="consoleName")
    def console_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the console
        """
        return pulumi.get(self, "console_name")

    @console_name.setter
    def console_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "console_name", value)


class Console(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 console_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ConsoleCreatePropertiesArgs']]] = None,
                 __props__=None):
        """
        Cloud shell console

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] console_name: The name of the console
        :param pulumi.Input[pulumi.InputType['ConsoleCreatePropertiesArgs']] properties: Cloud shell properties for creating a console.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConsoleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Cloud shell console

        :param str resource_name: The name of the resource.
        :param ConsoleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConsoleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 console_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ConsoleCreatePropertiesArgs']]] = None,
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
            __props__ = ConsoleArgs.__new__(ConsoleArgs)

            __props__.__dict__["console_name"] = console_name
            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__["properties"] = properties
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:portal:Console")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Console, __self__).__init__(
            'azure-native:portal/v20181001:Console',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Console':
        """
        Get an existing Console resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConsoleArgs.__new__(ConsoleArgs)

        __props__.__dict__["properties"] = None
        return Console(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ConsolePropertiesResponse']:
        """
        Cloud shell console properties.
        """
        return pulumi.get(self, "properties")

