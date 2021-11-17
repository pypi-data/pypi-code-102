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

__all__ = ['VirtualNetworkGatewayInitArgs', 'VirtualNetworkGateway']

@pulumi.input_type
class VirtualNetworkGatewayInitArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 bgp_settings: Optional[pulumi.Input['BgpSettingsArgs']] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 gateway_default_site: Optional[pulumi.Input['SubResourceArgs']] = None,
                 gateway_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayType']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkGatewayIPConfigurationArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['VirtualNetworkGatewaySkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_network_gateway_name: Optional[pulumi.Input[str]] = None,
                 vpn_client_configuration: Optional[pulumi.Input['VpnClientConfigurationArgs']] = None,
                 vpn_type: Optional[pulumi.Input[Union[str, 'VpnType']]] = None):
        """
        The set of arguments for constructing a VirtualNetworkGateway resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['BgpSettingsArgs'] bgp_settings: Virtual network gateway's BGP speaker settings
        :param pulumi.Input[bool] enable_bgp: EnableBgp Flag
        :param pulumi.Input[str] etag: Gets a unique read-only string that changes whenever the resource is updated
        :param pulumi.Input['SubResourceArgs'] gateway_default_site: Gets or sets the reference of the LocalNetworkGateway resource which represents Local network site having default routes. Assign Null value in case of removing existing default site setting.
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayType']] gateway_type: The type of this virtual network gateway.
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[Sequence[pulumi.Input['VirtualNetworkGatewayIPConfigurationArgs']]] ip_configurations: IpConfigurations for Virtual network gateway.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] provisioning_state: Gets or sets Provisioning state of the VirtualNetworkGateway resource Updating/Deleting/Failed
        :param pulumi.Input[str] resource_guid: Gets or sets resource GUID property of the VirtualNetworkGateway resource
        :param pulumi.Input['VirtualNetworkGatewaySkuArgs'] sku: Gets or sets the reference of the VirtualNetworkGatewaySku resource which represents the sku selected for Virtual network gateway.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] virtual_network_gateway_name: The name of the virtual network gateway.
        :param pulumi.Input['VpnClientConfigurationArgs'] vpn_client_configuration: Gets or sets the reference of the VpnClientConfiguration resource which represents the P2S VpnClient configurations.
        :param pulumi.Input[Union[str, 'VpnType']] vpn_type: The type of this virtual network gateway.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if bgp_settings is not None:
            pulumi.set(__self__, "bgp_settings", bgp_settings)
        if enable_bgp is not None:
            pulumi.set(__self__, "enable_bgp", enable_bgp)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if gateway_default_site is not None:
            pulumi.set(__self__, "gateway_default_site", gateway_default_site)
        if gateway_type is not None:
            pulumi.set(__self__, "gateway_type", gateway_type)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ip_configurations is not None:
            pulumi.set(__self__, "ip_configurations", ip_configurations)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_guid is not None:
            pulumi.set(__self__, "resource_guid", resource_guid)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if virtual_network_gateway_name is not None:
            pulumi.set(__self__, "virtual_network_gateway_name", virtual_network_gateway_name)
        if vpn_client_configuration is not None:
            pulumi.set(__self__, "vpn_client_configuration", vpn_client_configuration)
        if vpn_type is not None:
            pulumi.set(__self__, "vpn_type", vpn_type)

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
    @pulumi.getter(name="bgpSettings")
    def bgp_settings(self) -> Optional[pulumi.Input['BgpSettingsArgs']]:
        """
        Virtual network gateway's BGP speaker settings
        """
        return pulumi.get(self, "bgp_settings")

    @bgp_settings.setter
    def bgp_settings(self, value: Optional[pulumi.Input['BgpSettingsArgs']]):
        pulumi.set(self, "bgp_settings", value)

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> Optional[pulumi.Input[bool]]:
        """
        EnableBgp Flag
        """
        return pulumi.get(self, "enable_bgp")

    @enable_bgp.setter
    def enable_bgp(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_bgp", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        Gets a unique read-only string that changes whenever the resource is updated
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter(name="gatewayDefaultSite")
    def gateway_default_site(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        Gets or sets the reference of the LocalNetworkGateway resource which represents Local network site having default routes. Assign Null value in case of removing existing default site setting.
        """
        return pulumi.get(self, "gateway_default_site")

    @gateway_default_site.setter
    def gateway_default_site(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "gateway_default_site", value)

    @property
    @pulumi.getter(name="gatewayType")
    def gateway_type(self) -> Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayType']]]:
        """
        The type of this virtual network gateway.
        """
        return pulumi.get(self, "gateway_type")

    @gateway_type.setter
    def gateway_type(self, value: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayType']]]):
        pulumi.set(self, "gateway_type", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkGatewayIPConfigurationArgs']]]]:
        """
        IpConfigurations for Virtual network gateway.
        """
        return pulumi.get(self, "ip_configurations")

    @ip_configurations.setter
    def ip_configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkGatewayIPConfigurationArgs']]]]):
        pulumi.set(self, "ip_configurations", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets Provisioning state of the VirtualNetworkGateway resource Updating/Deleting/Failed
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets resource GUID property of the VirtualNetworkGateway resource
        """
        return pulumi.get(self, "resource_guid")

    @resource_guid.setter
    def resource_guid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_guid", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['VirtualNetworkGatewaySkuArgs']]:
        """
        Gets or sets the reference of the VirtualNetworkGatewaySku resource which represents the sku selected for Virtual network gateway.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['VirtualNetworkGatewaySkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="virtualNetworkGatewayName")
    def virtual_network_gateway_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the virtual network gateway.
        """
        return pulumi.get(self, "virtual_network_gateway_name")

    @virtual_network_gateway_name.setter
    def virtual_network_gateway_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_network_gateway_name", value)

    @property
    @pulumi.getter(name="vpnClientConfiguration")
    def vpn_client_configuration(self) -> Optional[pulumi.Input['VpnClientConfigurationArgs']]:
        """
        Gets or sets the reference of the VpnClientConfiguration resource which represents the P2S VpnClient configurations.
        """
        return pulumi.get(self, "vpn_client_configuration")

    @vpn_client_configuration.setter
    def vpn_client_configuration(self, value: Optional[pulumi.Input['VpnClientConfigurationArgs']]):
        pulumi.set(self, "vpn_client_configuration", value)

    @property
    @pulumi.getter(name="vpnType")
    def vpn_type(self) -> Optional[pulumi.Input[Union[str, 'VpnType']]]:
        """
        The type of this virtual network gateway.
        """
        return pulumi.get(self, "vpn_type")

    @vpn_type.setter
    def vpn_type(self, value: Optional[pulumi.Input[Union[str, 'VpnType']]]):
        pulumi.set(self, "vpn_type", value)


class VirtualNetworkGateway(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bgp_settings: Optional[pulumi.Input[pulumi.InputType['BgpSettingsArgs']]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 gateway_default_site: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 gateway_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayType']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualNetworkGatewayIPConfigurationArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkGatewaySkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_network_gateway_name: Optional[pulumi.Input[str]] = None,
                 vpn_client_configuration: Optional[pulumi.Input[pulumi.InputType['VpnClientConfigurationArgs']]] = None,
                 vpn_type: Optional[pulumi.Input[Union[str, 'VpnType']]] = None,
                 __props__=None):
        """
        A common class for general resource information

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['BgpSettingsArgs']] bgp_settings: Virtual network gateway's BGP speaker settings
        :param pulumi.Input[bool] enable_bgp: EnableBgp Flag
        :param pulumi.Input[str] etag: Gets a unique read-only string that changes whenever the resource is updated
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] gateway_default_site: Gets or sets the reference of the LocalNetworkGateway resource which represents Local network site having default routes. Assign Null value in case of removing existing default site setting.
        :param pulumi.Input[Union[str, 'VirtualNetworkGatewayType']] gateway_type: The type of this virtual network gateway.
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualNetworkGatewayIPConfigurationArgs']]]] ip_configurations: IpConfigurations for Virtual network gateway.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] provisioning_state: Gets or sets Provisioning state of the VirtualNetworkGateway resource Updating/Deleting/Failed
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_guid: Gets or sets resource GUID property of the VirtualNetworkGateway resource
        :param pulumi.Input[pulumi.InputType['VirtualNetworkGatewaySkuArgs']] sku: Gets or sets the reference of the VirtualNetworkGatewaySku resource which represents the sku selected for Virtual network gateway.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] virtual_network_gateway_name: The name of the virtual network gateway.
        :param pulumi.Input[pulumi.InputType['VpnClientConfigurationArgs']] vpn_client_configuration: Gets or sets the reference of the VpnClientConfiguration resource which represents the P2S VpnClient configurations.
        :param pulumi.Input[Union[str, 'VpnType']] vpn_type: The type of this virtual network gateway.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VirtualNetworkGatewayInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A common class for general resource information

        :param str resource_name: The name of the resource.
        :param VirtualNetworkGatewayInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VirtualNetworkGatewayInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bgp_settings: Optional[pulumi.Input[pulumi.InputType['BgpSettingsArgs']]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 gateway_default_site: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 gateway_type: Optional[pulumi.Input[Union[str, 'VirtualNetworkGatewayType']]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualNetworkGatewayIPConfigurationArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkGatewaySkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_network_gateway_name: Optional[pulumi.Input[str]] = None,
                 vpn_client_configuration: Optional[pulumi.Input[pulumi.InputType['VpnClientConfigurationArgs']]] = None,
                 vpn_type: Optional[pulumi.Input[Union[str, 'VpnType']]] = None,
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
            __props__ = VirtualNetworkGatewayInitArgs.__new__(VirtualNetworkGatewayInitArgs)

            __props__.__dict__["bgp_settings"] = bgp_settings
            __props__.__dict__["enable_bgp"] = enable_bgp
            __props__.__dict__["etag"] = etag
            __props__.__dict__["gateway_default_site"] = gateway_default_site
            __props__.__dict__["gateway_type"] = gateway_type
            __props__.__dict__["id"] = id
            __props__.__dict__["ip_configurations"] = ip_configurations
            __props__.__dict__["location"] = location
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_guid"] = resource_guid
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["virtual_network_gateway_name"] = virtual_network_gateway_name
            __props__.__dict__["vpn_client_configuration"] = vpn_client_configuration
            __props__.__dict__["vpn_type"] = vpn_type
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20150615:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20160601:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20160901:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20161201:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20170301:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20170601:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20170801:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20170901:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20171001:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20171101:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20180101:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20180201:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20180401:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20180601:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20180701:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20180801:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20181001:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20181101:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20181201:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20190201:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20190401:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20190601:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20190701:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20190801:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20190901:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20191101:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20191201:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20200301:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20200401:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20200501:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20200601:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20200701:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20200801:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20201101:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20210201:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20210301:VirtualNetworkGateway"), pulumi.Alias(type_="azure-native:network/v20210501:VirtualNetworkGateway")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualNetworkGateway, __self__).__init__(
            'azure-native:network/v20160330:VirtualNetworkGateway',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualNetworkGateway':
        """
        Get an existing VirtualNetworkGateway resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VirtualNetworkGatewayInitArgs.__new__(VirtualNetworkGatewayInitArgs)

        __props__.__dict__["bgp_settings"] = None
        __props__.__dict__["enable_bgp"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["gateway_default_site"] = None
        __props__.__dict__["gateway_type"] = None
        __props__.__dict__["ip_configurations"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_guid"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["vpn_client_configuration"] = None
        __props__.__dict__["vpn_type"] = None
        return VirtualNetworkGateway(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bgpSettings")
    def bgp_settings(self) -> pulumi.Output[Optional['outputs.BgpSettingsResponse']]:
        """
        Virtual network gateway's BGP speaker settings
        """
        return pulumi.get(self, "bgp_settings")

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> pulumi.Output[Optional[bool]]:
        """
        EnableBgp Flag
        """
        return pulumi.get(self, "enable_bgp")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Gets a unique read-only string that changes whenever the resource is updated
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="gatewayDefaultSite")
    def gateway_default_site(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Gets or sets the reference of the LocalNetworkGateway resource which represents Local network site having default routes. Assign Null value in case of removing existing default site setting.
        """
        return pulumi.get(self, "gateway_default_site")

    @property
    @pulumi.getter(name="gatewayType")
    def gateway_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of this virtual network gateway.
        """
        return pulumi.get(self, "gateway_type")

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> pulumi.Output[Optional[Sequence['outputs.VirtualNetworkGatewayIPConfigurationResponse']]]:
        """
        IpConfigurations for Virtual network gateway.
        """
        return pulumi.get(self, "ip_configurations")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets Provisioning state of the VirtualNetworkGateway resource Updating/Deleting/Failed
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets resource GUID property of the VirtualNetworkGateway resource
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.VirtualNetworkGatewaySkuResponse']]:
        """
        Gets or sets the reference of the VirtualNetworkGatewaySku resource which represents the sku selected for Virtual network gateway.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vpnClientConfiguration")
    def vpn_client_configuration(self) -> pulumi.Output[Optional['outputs.VpnClientConfigurationResponse']]:
        """
        Gets or sets the reference of the VpnClientConfiguration resource which represents the P2S VpnClient configurations.
        """
        return pulumi.get(self, "vpn_client_configuration")

    @property
    @pulumi.getter(name="vpnType")
    def vpn_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of this virtual network gateway.
        """
        return pulumi.get(self, "vpn_type")

