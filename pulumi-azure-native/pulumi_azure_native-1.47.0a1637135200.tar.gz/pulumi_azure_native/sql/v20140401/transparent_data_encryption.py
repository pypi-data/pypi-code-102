# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['TransparentDataEncryptionArgs', 'TransparentDataEncryption']

@pulumi.input_type
class TransparentDataEncryptionArgs:
    def __init__(__self__, *,
                 database_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 status: Optional[pulumi.Input[Union[str, 'TransparentDataEncryptionStatus']]] = None,
                 transparent_data_encryption_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a TransparentDataEncryption resource.
        :param pulumi.Input[str] database_name: The name of the database for which setting the transparent data encryption applies.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[Union[str, 'TransparentDataEncryptionStatus']] status: The status of the database transparent data encryption.
        :param pulumi.Input[str] transparent_data_encryption_name: The name of the transparent data encryption configuration.
        """
        pulumi.set(__self__, "database_name", database_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server_name", server_name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if transparent_data_encryption_name is not None:
            pulumi.set(__self__, "transparent_data_encryption_name", transparent_data_encryption_name)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Input[str]:
        """
        The name of the database for which setting the transparent data encryption applies.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> pulumi.Input[str]:
        """
        The name of the server.
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'TransparentDataEncryptionStatus']]]:
        """
        The status of the database transparent data encryption.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'TransparentDataEncryptionStatus']]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="transparentDataEncryptionName")
    def transparent_data_encryption_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the transparent data encryption configuration.
        """
        return pulumi.get(self, "transparent_data_encryption_name")

    @transparent_data_encryption_name.setter
    def transparent_data_encryption_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transparent_data_encryption_name", value)


class TransparentDataEncryption(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'TransparentDataEncryptionStatus']]] = None,
                 transparent_data_encryption_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a database transparent data encryption configuration.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database_name: The name of the database for which setting the transparent data encryption applies.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[Union[str, 'TransparentDataEncryptionStatus']] status: The status of the database transparent data encryption.
        :param pulumi.Input[str] transparent_data_encryption_name: The name of the transparent data encryption configuration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TransparentDataEncryptionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a database transparent data encryption configuration.

        :param str resource_name: The name of the resource.
        :param TransparentDataEncryptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TransparentDataEncryptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'TransparentDataEncryptionStatus']]] = None,
                 transparent_data_encryption_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = TransparentDataEncryptionArgs.__new__(TransparentDataEncryptionArgs)

            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__["database_name"] = database_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["status"] = status
            __props__.__dict__["transparent_data_encryption_name"] = transparent_data_encryption_name
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:TransparentDataEncryption"), pulumi.Alias(type_="azure-native:sql/v20200202preview:TransparentDataEncryption"), pulumi.Alias(type_="azure-native:sql/v20200801preview:TransparentDataEncryption"), pulumi.Alias(type_="azure-native:sql/v20201101preview:TransparentDataEncryption"), pulumi.Alias(type_="azure-native:sql/v20210201preview:TransparentDataEncryption"), pulumi.Alias(type_="azure-native:sql/v20210501preview:TransparentDataEncryption")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(TransparentDataEncryption, __self__).__init__(
            'azure-native:sql/v20140401:TransparentDataEncryption',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'TransparentDataEncryption':
        """
        Get an existing TransparentDataEncryption resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = TransparentDataEncryptionArgs.__new__(TransparentDataEncryptionArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["type"] = None
        return TransparentDataEncryption(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        The status of the database transparent data encryption.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

