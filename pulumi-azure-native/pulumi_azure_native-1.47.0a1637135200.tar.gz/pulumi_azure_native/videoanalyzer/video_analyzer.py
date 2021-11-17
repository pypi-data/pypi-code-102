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

__all__ = ['VideoAnalyzerArgs', 'VideoAnalyzer']

@pulumi.input_type
class VideoAnalyzerArgs:
    def __init__(__self__, *,
                 encryption: pulumi.Input['AccountEncryptionArgs'],
                 resource_group_name: pulumi.Input[str],
                 storage_accounts: pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]],
                 account_name: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['VideoAnalyzerIdentityArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a VideoAnalyzer resource.
        :param pulumi.Input['AccountEncryptionArgs'] encryption: The account encryption properties.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]] storage_accounts: The storage accounts for this resource.
        :param pulumi.Input[str] account_name: The Video Analyzer account name.
        :param pulumi.Input['VideoAnalyzerIdentityArgs'] identity: The set of managed identities associated with the Video Analyzer resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "encryption", encryption)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "storage_accounts", storage_accounts)
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def encryption(self) -> pulumi.Input['AccountEncryptionArgs']:
        """
        The account encryption properties.
        """
        return pulumi.get(self, "encryption")

    @encryption.setter
    def encryption(self, value: pulumi.Input['AccountEncryptionArgs']):
        pulumi.set(self, "encryption", value)

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
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]]:
        """
        The storage accounts for this resource.
        """
        return pulumi.get(self, "storage_accounts")

    @storage_accounts.setter
    def storage_accounts(self, value: pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]]):
        pulumi.set(self, "storage_accounts", value)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Video Analyzer account name.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['VideoAnalyzerIdentityArgs']]:
        """
        The set of managed identities associated with the Video Analyzer resource.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['VideoAnalyzerIdentityArgs']]):
        pulumi.set(self, "identity", value)

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
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class VideoAnalyzer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['AccountEncryptionArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['VideoAnalyzerIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StorageAccountArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        A Video Analyzer account.
        API Version: 2021-05-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The Video Analyzer account name.
        :param pulumi.Input[pulumi.InputType['AccountEncryptionArgs']] encryption: The account encryption properties.
        :param pulumi.Input[pulumi.InputType['VideoAnalyzerIdentityArgs']] identity: The set of managed identities associated with the Video Analyzer resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StorageAccountArgs']]]] storage_accounts: The storage accounts for this resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VideoAnalyzerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A Video Analyzer account.
        API Version: 2021-05-01-preview.

        :param str resource_name: The name of the resource.
        :param VideoAnalyzerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VideoAnalyzerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['AccountEncryptionArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['VideoAnalyzerIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StorageAccountArgs']]]]] = None,
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
            __props__ = VideoAnalyzerArgs.__new__(VideoAnalyzerArgs)

            __props__.__dict__["account_name"] = account_name
            if encryption is None and not opts.urn:
                raise TypeError("Missing required property 'encryption'")
            __props__.__dict__["encryption"] = encryption
            __props__.__dict__["identity"] = identity
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if storage_accounts is None and not opts.urn:
                raise TypeError("Missing required property 'storage_accounts'")
            __props__.__dict__["storage_accounts"] = storage_accounts
            __props__.__dict__["tags"] = tags
            __props__.__dict__["endpoints"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:videoanalyzer/v20210501preview:VideoAnalyzer"), pulumi.Alias(type_="azure-native:videoanalyzer/v20211101preview:VideoAnalyzer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VideoAnalyzer, __self__).__init__(
            'azure-native:videoanalyzer:VideoAnalyzer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VideoAnalyzer':
        """
        Get an existing VideoAnalyzer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VideoAnalyzerArgs.__new__(VideoAnalyzerArgs)

        __props__.__dict__["encryption"] = None
        __props__.__dict__["endpoints"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["storage_accounts"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return VideoAnalyzer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def encryption(self) -> pulumi.Output['outputs.AccountEncryptionResponse']:
        """
        The account encryption properties.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def endpoints(self) -> pulumi.Output[Sequence['outputs.EndpointResponse']]:
        """
        The list of endpoints associated with this resource.
        """
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.VideoAnalyzerIdentityResponse']]:
        """
        The set of managed identities associated with the Video Analyzer resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> pulumi.Output[Sequence['outputs.StorageAccountResponse']]:
        """
        The storage accounts for this resource.
        """
        return pulumi.get(self, "storage_accounts")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system data of the Video Analyzer account.
        """
        return pulumi.get(self, "system_data")

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

