# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['NetworkWatcherArgs', 'NetworkWatcher']

@pulumi.input_type
class NetworkWatcherArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_watcher_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NetworkWatcher resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] network_watcher_name: The name of the network watcher.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_watcher_name is not None:
            pulumi.set(__self__, "network_watcher_name", network_watcher_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

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
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="networkWatcherName")
    def network_watcher_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the network watcher.
        """
        return pulumi.get(self, "network_watcher_name")

    @network_watcher_name.setter
    def network_watcher_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_watcher_name", value)

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


class NetworkWatcher(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_watcher_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Network watcher in a resource group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] network_watcher_name: The name of the network watcher.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkWatcherArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Network watcher in a resource group.

        :param str resource_name: The name of the resource.
        :param NetworkWatcherArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkWatcherArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_watcher_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = NetworkWatcherArgs.__new__(NetworkWatcherArgs)

            __props__.__dict__["etag"] = etag
            __props__.__dict__["id"] = id
            __props__.__dict__["location"] = location
            __props__.__dict__["network_watcher_name"] = network_watcher_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20160901:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20161201:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20170301:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20170601:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20170801:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20170901:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20171001:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20171101:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20180101:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20180201:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20180401:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20180601:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20180701:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20180801:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20181001:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20181101:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20181201:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20190201:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20190401:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20190601:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20190701:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20190901:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20191101:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20191201:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20200301:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20200401:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20200501:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20200601:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20200701:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20200801:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20201101:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20210201:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20210301:NetworkWatcher"), pulumi.Alias(type_="azure-native:network/v20210501:NetworkWatcher")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NetworkWatcher, __self__).__init__(
            'azure-native:network/v20190801:NetworkWatcher',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NetworkWatcher':
        """
        Get an existing NetworkWatcher resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkWatcherArgs.__new__(NetworkWatcherArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return NetworkWatcher(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the network watcher resource.
        """
        return pulumi.get(self, "provisioning_state")

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
        Resource type.
        """
        return pulumi.get(self, "type")

