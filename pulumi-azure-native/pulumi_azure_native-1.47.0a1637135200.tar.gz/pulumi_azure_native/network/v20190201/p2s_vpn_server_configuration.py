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

__all__ = ['P2sVpnServerConfigurationArgs', 'P2sVpnServerConfiguration']

@pulumi.input_type
class P2sVpnServerConfigurationArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 virtual_wan_name: pulumi.Input[str],
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 p2_s_vpn_server_config_radius_client_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusClientRootCertificateArgs']]]] = None,
                 p2_s_vpn_server_config_radius_server_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusServerRootCertificateArgs']]]] = None,
                 p2_s_vpn_server_config_vpn_client_revoked_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRevokedCertificateArgs']]]] = None,
                 p2_s_vpn_server_config_vpn_client_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRootCertificateArgs']]]] = None,
                 p2_s_vpn_server_configuration_name: Optional[pulumi.Input[str]] = None,
                 radius_server_address: Optional[pulumi.Input[str]] = None,
                 radius_server_secret: Optional[pulumi.Input[str]] = None,
                 vpn_client_ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]] = None,
                 vpn_protocols: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'VpnGatewayTunnelingProtocol']]]]] = None):
        """
        The set of arguments for constructing a P2sVpnServerConfiguration resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualWan.
        :param pulumi.Input[str] virtual_wan_name: The name of the VirtualWan.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the P2SVpnServerConfiguration that is unique within a VirtualWan in a resource group. This name can be used to access the resource along with Paren VirtualWan resource name.
        :param pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusClientRootCertificateArgs']]] p2_s_vpn_server_config_radius_client_root_certificates: Radius client root certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusServerRootCertificateArgs']]] p2_s_vpn_server_config_radius_server_root_certificates: Radius Server root certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRevokedCertificateArgs']]] p2_s_vpn_server_config_vpn_client_revoked_certificates: VPN client revoked certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRootCertificateArgs']]] p2_s_vpn_server_config_vpn_client_root_certificates: VPN client root certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[str] p2_s_vpn_server_configuration_name: The name of the P2SVpnServerConfiguration.
        :param pulumi.Input[str] radius_server_address: The radius server address property of the P2SVpnServerConfiguration resource for point to site client connection.
        :param pulumi.Input[str] radius_server_secret: The radius secret property of the P2SVpnServerConfiguration resource for point to site client connection.
        :param pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]] vpn_client_ipsec_policies: VpnClientIpsecPolicies for P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'VpnGatewayTunnelingProtocol']]]] vpn_protocols: VPN protocols for the P2SVpnServerConfiguration.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "virtual_wan_name", virtual_wan_name)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if p2_s_vpn_server_config_radius_client_root_certificates is not None:
            pulumi.set(__self__, "p2_s_vpn_server_config_radius_client_root_certificates", p2_s_vpn_server_config_radius_client_root_certificates)
        if p2_s_vpn_server_config_radius_server_root_certificates is not None:
            pulumi.set(__self__, "p2_s_vpn_server_config_radius_server_root_certificates", p2_s_vpn_server_config_radius_server_root_certificates)
        if p2_s_vpn_server_config_vpn_client_revoked_certificates is not None:
            pulumi.set(__self__, "p2_s_vpn_server_config_vpn_client_revoked_certificates", p2_s_vpn_server_config_vpn_client_revoked_certificates)
        if p2_s_vpn_server_config_vpn_client_root_certificates is not None:
            pulumi.set(__self__, "p2_s_vpn_server_config_vpn_client_root_certificates", p2_s_vpn_server_config_vpn_client_root_certificates)
        if p2_s_vpn_server_configuration_name is not None:
            pulumi.set(__self__, "p2_s_vpn_server_configuration_name", p2_s_vpn_server_configuration_name)
        if radius_server_address is not None:
            pulumi.set(__self__, "radius_server_address", radius_server_address)
        if radius_server_secret is not None:
            pulumi.set(__self__, "radius_server_secret", radius_server_secret)
        if vpn_client_ipsec_policies is not None:
            pulumi.set(__self__, "vpn_client_ipsec_policies", vpn_client_ipsec_policies)
        if vpn_protocols is not None:
            pulumi.set(__self__, "vpn_protocols", vpn_protocols)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name of the VirtualWan.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="virtualWanName")
    def virtual_wan_name(self) -> pulumi.Input[str]:
        """
        The name of the VirtualWan.
        """
        return pulumi.get(self, "virtual_wan_name")

    @virtual_wan_name.setter
    def virtual_wan_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_wan_name", value)

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
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the P2SVpnServerConfiguration that is unique within a VirtualWan in a resource group. This name can be used to access the resource along with Paren VirtualWan resource name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="p2SVpnServerConfigRadiusClientRootCertificates")
    def p2_s_vpn_server_config_radius_client_root_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusClientRootCertificateArgs']]]]:
        """
        Radius client root certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_radius_client_root_certificates")

    @p2_s_vpn_server_config_radius_client_root_certificates.setter
    def p2_s_vpn_server_config_radius_client_root_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusClientRootCertificateArgs']]]]):
        pulumi.set(self, "p2_s_vpn_server_config_radius_client_root_certificates", value)

    @property
    @pulumi.getter(name="p2SVpnServerConfigRadiusServerRootCertificates")
    def p2_s_vpn_server_config_radius_server_root_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusServerRootCertificateArgs']]]]:
        """
        Radius Server root certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_radius_server_root_certificates")

    @p2_s_vpn_server_config_radius_server_root_certificates.setter
    def p2_s_vpn_server_config_radius_server_root_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigRadiusServerRootCertificateArgs']]]]):
        pulumi.set(self, "p2_s_vpn_server_config_radius_server_root_certificates", value)

    @property
    @pulumi.getter(name="p2SVpnServerConfigVpnClientRevokedCertificates")
    def p2_s_vpn_server_config_vpn_client_revoked_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRevokedCertificateArgs']]]]:
        """
        VPN client revoked certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_vpn_client_revoked_certificates")

    @p2_s_vpn_server_config_vpn_client_revoked_certificates.setter
    def p2_s_vpn_server_config_vpn_client_revoked_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRevokedCertificateArgs']]]]):
        pulumi.set(self, "p2_s_vpn_server_config_vpn_client_revoked_certificates", value)

    @property
    @pulumi.getter(name="p2SVpnServerConfigVpnClientRootCertificates")
    def p2_s_vpn_server_config_vpn_client_root_certificates(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRootCertificateArgs']]]]:
        """
        VPN client root certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_vpn_client_root_certificates")

    @p2_s_vpn_server_config_vpn_client_root_certificates.setter
    def p2_s_vpn_server_config_vpn_client_root_certificates(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['P2SVpnServerConfigVpnClientRootCertificateArgs']]]]):
        pulumi.set(self, "p2_s_vpn_server_config_vpn_client_root_certificates", value)

    @property
    @pulumi.getter(name="p2SVpnServerConfigurationName")
    def p2_s_vpn_server_configuration_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_configuration_name")

    @p2_s_vpn_server_configuration_name.setter
    def p2_s_vpn_server_configuration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "p2_s_vpn_server_configuration_name", value)

    @property
    @pulumi.getter(name="radiusServerAddress")
    def radius_server_address(self) -> Optional[pulumi.Input[str]]:
        """
        The radius server address property of the P2SVpnServerConfiguration resource for point to site client connection.
        """
        return pulumi.get(self, "radius_server_address")

    @radius_server_address.setter
    def radius_server_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "radius_server_address", value)

    @property
    @pulumi.getter(name="radiusServerSecret")
    def radius_server_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The radius secret property of the P2SVpnServerConfiguration resource for point to site client connection.
        """
        return pulumi.get(self, "radius_server_secret")

    @radius_server_secret.setter
    def radius_server_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "radius_server_secret", value)

    @property
    @pulumi.getter(name="vpnClientIpsecPolicies")
    def vpn_client_ipsec_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]]:
        """
        VpnClientIpsecPolicies for P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "vpn_client_ipsec_policies")

    @vpn_client_ipsec_policies.setter
    def vpn_client_ipsec_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IpsecPolicyArgs']]]]):
        pulumi.set(self, "vpn_client_ipsec_policies", value)

    @property
    @pulumi.getter(name="vpnProtocols")
    def vpn_protocols(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'VpnGatewayTunnelingProtocol']]]]]:
        """
        VPN protocols for the P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "vpn_protocols")

    @vpn_protocols.setter
    def vpn_protocols(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'VpnGatewayTunnelingProtocol']]]]]):
        pulumi.set(self, "vpn_protocols", value)


class P2sVpnServerConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 p2_s_vpn_server_config_radius_client_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigRadiusClientRootCertificateArgs']]]]] = None,
                 p2_s_vpn_server_config_radius_server_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigRadiusServerRootCertificateArgs']]]]] = None,
                 p2_s_vpn_server_config_vpn_client_revoked_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigVpnClientRevokedCertificateArgs']]]]] = None,
                 p2_s_vpn_server_config_vpn_client_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigVpnClientRootCertificateArgs']]]]] = None,
                 p2_s_vpn_server_configuration_name: Optional[pulumi.Input[str]] = None,
                 radius_server_address: Optional[pulumi.Input[str]] = None,
                 radius_server_secret: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 virtual_wan_name: Optional[pulumi.Input[str]] = None,
                 vpn_client_ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]]] = None,
                 vpn_protocols: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'VpnGatewayTunnelingProtocol']]]]] = None,
                 __props__=None):
        """
        P2SVpnServerConfiguration Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the P2SVpnServerConfiguration that is unique within a VirtualWan in a resource group. This name can be used to access the resource along with Paren VirtualWan resource name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigRadiusClientRootCertificateArgs']]]] p2_s_vpn_server_config_radius_client_root_certificates: Radius client root certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigRadiusServerRootCertificateArgs']]]] p2_s_vpn_server_config_radius_server_root_certificates: Radius Server root certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigVpnClientRevokedCertificateArgs']]]] p2_s_vpn_server_config_vpn_client_revoked_certificates: VPN client revoked certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigVpnClientRootCertificateArgs']]]] p2_s_vpn_server_config_vpn_client_root_certificates: VPN client root certificate of P2SVpnServerConfiguration.
        :param pulumi.Input[str] p2_s_vpn_server_configuration_name: The name of the P2SVpnServerConfiguration.
        :param pulumi.Input[str] radius_server_address: The radius server address property of the P2SVpnServerConfiguration resource for point to site client connection.
        :param pulumi.Input[str] radius_server_secret: The radius secret property of the P2SVpnServerConfiguration resource for point to site client connection.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualWan.
        :param pulumi.Input[str] virtual_wan_name: The name of the VirtualWan.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]] vpn_client_ipsec_policies: VpnClientIpsecPolicies for P2SVpnServerConfiguration.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'VpnGatewayTunnelingProtocol']]]] vpn_protocols: VPN protocols for the P2SVpnServerConfiguration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: P2sVpnServerConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        P2SVpnServerConfiguration Resource.

        :param str resource_name: The name of the resource.
        :param P2sVpnServerConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(P2sVpnServerConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 p2_s_vpn_server_config_radius_client_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigRadiusClientRootCertificateArgs']]]]] = None,
                 p2_s_vpn_server_config_radius_server_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigRadiusServerRootCertificateArgs']]]]] = None,
                 p2_s_vpn_server_config_vpn_client_revoked_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigVpnClientRevokedCertificateArgs']]]]] = None,
                 p2_s_vpn_server_config_vpn_client_root_certificates: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['P2SVpnServerConfigVpnClientRootCertificateArgs']]]]] = None,
                 p2_s_vpn_server_configuration_name: Optional[pulumi.Input[str]] = None,
                 radius_server_address: Optional[pulumi.Input[str]] = None,
                 radius_server_secret: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 virtual_wan_name: Optional[pulumi.Input[str]] = None,
                 vpn_client_ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]]] = None,
                 vpn_protocols: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'VpnGatewayTunnelingProtocol']]]]] = None,
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
            __props__ = P2sVpnServerConfigurationArgs.__new__(P2sVpnServerConfigurationArgs)

            __props__.__dict__["etag"] = etag
            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            __props__.__dict__["p2_s_vpn_server_config_radius_client_root_certificates"] = p2_s_vpn_server_config_radius_client_root_certificates
            __props__.__dict__["p2_s_vpn_server_config_radius_server_root_certificates"] = p2_s_vpn_server_config_radius_server_root_certificates
            __props__.__dict__["p2_s_vpn_server_config_vpn_client_revoked_certificates"] = p2_s_vpn_server_config_vpn_client_revoked_certificates
            __props__.__dict__["p2_s_vpn_server_config_vpn_client_root_certificates"] = p2_s_vpn_server_config_vpn_client_root_certificates
            __props__.__dict__["p2_s_vpn_server_configuration_name"] = p2_s_vpn_server_configuration_name
            __props__.__dict__["radius_server_address"] = radius_server_address
            __props__.__dict__["radius_server_secret"] = radius_server_secret
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if virtual_wan_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_wan_name'")
            __props__.__dict__["virtual_wan_name"] = virtual_wan_name
            __props__.__dict__["vpn_client_ipsec_policies"] = vpn_client_ipsec_policies
            __props__.__dict__["vpn_protocols"] = vpn_protocols
            __props__.__dict__["p2_s_vpn_gateways"] = None
            __props__.__dict__["provisioning_state"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:P2sVpnServerConfiguration"), pulumi.Alias(type_="azure-native:network/v20180801:P2sVpnServerConfiguration"), pulumi.Alias(type_="azure-native:network/v20181001:P2sVpnServerConfiguration"), pulumi.Alias(type_="azure-native:network/v20181101:P2sVpnServerConfiguration"), pulumi.Alias(type_="azure-native:network/v20181201:P2sVpnServerConfiguration"), pulumi.Alias(type_="azure-native:network/v20190401:P2sVpnServerConfiguration"), pulumi.Alias(type_="azure-native:network/v20190601:P2sVpnServerConfiguration"), pulumi.Alias(type_="azure-native:network/v20190701:P2sVpnServerConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(P2sVpnServerConfiguration, __self__).__init__(
            'azure-native:network/v20190201:P2sVpnServerConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'P2sVpnServerConfiguration':
        """
        Get an existing P2sVpnServerConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = P2sVpnServerConfigurationArgs.__new__(P2sVpnServerConfigurationArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["p2_s_vpn_gateways"] = None
        __props__.__dict__["p2_s_vpn_server_config_radius_client_root_certificates"] = None
        __props__.__dict__["p2_s_vpn_server_config_radius_server_root_certificates"] = None
        __props__.__dict__["p2_s_vpn_server_config_vpn_client_revoked_certificates"] = None
        __props__.__dict__["p2_s_vpn_server_config_vpn_client_root_certificates"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["radius_server_address"] = None
        __props__.__dict__["radius_server_secret"] = None
        __props__.__dict__["vpn_client_ipsec_policies"] = None
        __props__.__dict__["vpn_protocols"] = None
        return P2sVpnServerConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the P2SVpnServerConfiguration that is unique within a VirtualWan in a resource group. This name can be used to access the resource along with Paren VirtualWan resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="p2SVpnGateways")
    def p2_s_vpn_gateways(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to P2SVpnGateways.
        """
        return pulumi.get(self, "p2_s_vpn_gateways")

    @property
    @pulumi.getter(name="p2SVpnServerConfigRadiusClientRootCertificates")
    def p2_s_vpn_server_config_radius_client_root_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.P2SVpnServerConfigRadiusClientRootCertificateResponse']]]:
        """
        Radius client root certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_radius_client_root_certificates")

    @property
    @pulumi.getter(name="p2SVpnServerConfigRadiusServerRootCertificates")
    def p2_s_vpn_server_config_radius_server_root_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.P2SVpnServerConfigRadiusServerRootCertificateResponse']]]:
        """
        Radius Server root certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_radius_server_root_certificates")

    @property
    @pulumi.getter(name="p2SVpnServerConfigVpnClientRevokedCertificates")
    def p2_s_vpn_server_config_vpn_client_revoked_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.P2SVpnServerConfigVpnClientRevokedCertificateResponse']]]:
        """
        VPN client revoked certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_vpn_client_revoked_certificates")

    @property
    @pulumi.getter(name="p2SVpnServerConfigVpnClientRootCertificates")
    def p2_s_vpn_server_config_vpn_client_root_certificates(self) -> pulumi.Output[Optional[Sequence['outputs.P2SVpnServerConfigVpnClientRootCertificateResponse']]]:
        """
        VPN client root certificate of P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "p2_s_vpn_server_config_vpn_client_root_certificates")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the P2SVpnServerConfiguration resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="radiusServerAddress")
    def radius_server_address(self) -> pulumi.Output[Optional[str]]:
        """
        The radius server address property of the P2SVpnServerConfiguration resource for point to site client connection.
        """
        return pulumi.get(self, "radius_server_address")

    @property
    @pulumi.getter(name="radiusServerSecret")
    def radius_server_secret(self) -> pulumi.Output[Optional[str]]:
        """
        The radius secret property of the P2SVpnServerConfiguration resource for point to site client connection.
        """
        return pulumi.get(self, "radius_server_secret")

    @property
    @pulumi.getter(name="vpnClientIpsecPolicies")
    def vpn_client_ipsec_policies(self) -> pulumi.Output[Optional[Sequence['outputs.IpsecPolicyResponse']]]:
        """
        VpnClientIpsecPolicies for P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "vpn_client_ipsec_policies")

    @property
    @pulumi.getter(name="vpnProtocols")
    def vpn_protocols(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        VPN protocols for the P2SVpnServerConfiguration.
        """
        return pulumi.get(self, "vpn_protocols")

