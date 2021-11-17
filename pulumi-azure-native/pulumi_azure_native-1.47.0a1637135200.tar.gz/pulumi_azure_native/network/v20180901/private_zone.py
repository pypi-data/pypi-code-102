# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['PrivateZoneArgs', 'PrivateZone']

@pulumi.input_type
class PrivateZoneArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_zone_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a PrivateZone resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] etag: The ETag of the zone.
        :param pulumi.Input[str] location: The Azure Region where the resource lives
        :param pulumi.Input[str] private_zone_name: The name of the Private DNS zone (without a terminating dot).
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if private_zone_name is not None:
            pulumi.set(__self__, "private_zone_name", private_zone_name)
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
        The ETag of the zone.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Region where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="privateZoneName")
    def private_zone_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Private DNS zone (without a terminating dot).
        """
        return pulumi.get(self, "private_zone_name")

    @private_zone_name.setter
    def private_zone_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_zone_name", value)

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


class PrivateZone(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_zone_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Describes a Private DNS zone.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: The ETag of the zone.
        :param pulumi.Input[str] location: The Azure Region where the resource lives
        :param pulumi.Input[str] private_zone_name: The name of the Private DNS zone (without a terminating dot).
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PrivateZoneArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a Private DNS zone.

        :param str resource_name: The name of the resource.
        :param PrivateZoneArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PrivateZoneArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_zone_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = PrivateZoneArgs.__new__(PrivateZoneArgs)

            __props__.__dict__["etag"] = etag
            __props__.__dict__["location"] = location
            __props__.__dict__["private_zone_name"] = private_zone_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["max_number_of_record_sets"] = None
            __props__.__dict__["max_number_of_virtual_network_links"] = None
            __props__.__dict__["max_number_of_virtual_network_links_with_registration"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["number_of_record_sets"] = None
            __props__.__dict__["number_of_virtual_network_links"] = None
            __props__.__dict__["number_of_virtual_network_links_with_registration"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:PrivateZone"), pulumi.Alias(type_="azure-native:network/v20200101:PrivateZone"), pulumi.Alias(type_="azure-native:network/v20200601:PrivateZone")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateZone, __self__).__init__(
            'azure-native:network/v20180901:PrivateZone',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrivateZone':
        """
        Get an existing PrivateZone resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PrivateZoneArgs.__new__(PrivateZoneArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["max_number_of_record_sets"] = None
        __props__.__dict__["max_number_of_virtual_network_links"] = None
        __props__.__dict__["max_number_of_virtual_network_links_with_registration"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["number_of_record_sets"] = None
        __props__.__dict__["number_of_virtual_network_links"] = None
        __props__.__dict__["number_of_virtual_network_links_with_registration"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return PrivateZone(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        The ETag of the zone.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The Azure Region where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxNumberOfRecordSets")
    def max_number_of_record_sets(self) -> pulumi.Output[float]:
        """
        The maximum number of record sets that can be created in this Private DNS zone. This is a read-only property and any attempt to set this value will be ignored.
        """
        return pulumi.get(self, "max_number_of_record_sets")

    @property
    @pulumi.getter(name="maxNumberOfVirtualNetworkLinks")
    def max_number_of_virtual_network_links(self) -> pulumi.Output[float]:
        """
        The maximum number of virtual networks that can be linked to this Private DNS zone. This is a read-only property and any attempt to set this value will be ignored.
        """
        return pulumi.get(self, "max_number_of_virtual_network_links")

    @property
    @pulumi.getter(name="maxNumberOfVirtualNetworkLinksWithRegistration")
    def max_number_of_virtual_network_links_with_registration(self) -> pulumi.Output[float]:
        """
        The maximum number of virtual networks that can be linked to this Private DNS zone with registration enabled. This is a read-only property and any attempt to set this value will be ignored.
        """
        return pulumi.get(self, "max_number_of_virtual_network_links_with_registration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numberOfRecordSets")
    def number_of_record_sets(self) -> pulumi.Output[float]:
        """
        The current number of record sets in this Private DNS zone. This is a read-only property and any attempt to set this value will be ignored.
        """
        return pulumi.get(self, "number_of_record_sets")

    @property
    @pulumi.getter(name="numberOfVirtualNetworkLinks")
    def number_of_virtual_network_links(self) -> pulumi.Output[float]:
        """
        The current number of virtual networks that are linked to this Private DNS zone. This is a read-only property and any attempt to set this value will be ignored.
        """
        return pulumi.get(self, "number_of_virtual_network_links")

    @property
    @pulumi.getter(name="numberOfVirtualNetworkLinksWithRegistration")
    def number_of_virtual_network_links_with_registration(self) -> pulumi.Output[float]:
        """
        The current number of virtual networks that are linked to this Private DNS zone with registration enabled. This is a read-only property and any attempt to set this value will be ignored.
        """
        return pulumi.get(self, "number_of_virtual_network_links_with_registration")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource. This is a read-only property and any attempt to set this value will be ignored.
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
        The type of the resource. Example - 'Microsoft.Network/privateDnsZones'.
        """
        return pulumi.get(self, "type")

