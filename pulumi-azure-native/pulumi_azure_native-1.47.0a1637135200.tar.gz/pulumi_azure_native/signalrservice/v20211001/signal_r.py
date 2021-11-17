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

__all__ = ['SignalRArgs', 'SignalR']

@pulumi.input_type
class SignalRArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 cors: Optional[pulumi.Input['SignalRCorsSettingsArgs']] = None,
                 disable_aad_auth: Optional[pulumi.Input[bool]] = None,
                 disable_local_auth: Optional[pulumi.Input[bool]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input['SignalRFeatureArgs']]]] = None,
                 identity: Optional[pulumi.Input['ManagedIdentityArgs']] = None,
                 kind: Optional[pulumi.Input[Union[str, 'ServiceKind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_acls: Optional[pulumi.Input['SignalRNetworkACLsArgs']] = None,
                 public_network_access: Optional[pulumi.Input[str]] = None,
                 resource_log_configuration: Optional[pulumi.Input['ResourceLogConfigurationArgs']] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['ResourceSkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tls: Optional[pulumi.Input['SignalRTlsSettingsArgs']] = None,
                 upstream: Optional[pulumi.Input['ServerlessUpstreamSettingsArgs']] = None):
        """
        The set of arguments for constructing a SignalR resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input['SignalRCorsSettingsArgs'] cors: Cross-Origin Resource Sharing (CORS) settings.
        :param pulumi.Input[bool] disable_aad_auth: DisableLocalAuth
               Enable or disable aad auth
               When set as true, connection with AuthType=aad won't work.
        :param pulumi.Input[bool] disable_local_auth: DisableLocalAuth
               Enable or disable local auth with AccessKey
               When set as true, connection with AccessKey=xxx won't work.
        :param pulumi.Input[Sequence[pulumi.Input['SignalRFeatureArgs']]] features: List of the featureFlags.
               
               FeatureFlags that are not included in the parameters for the update operation will not be modified.
               And the response will only include featureFlags that are explicitly set. 
               When a featureFlag is not explicitly set, its globally default value will be used
               But keep in mind, the default value doesn't mean "false". It varies in terms of different FeatureFlags.
        :param pulumi.Input['ManagedIdentityArgs'] identity: The managed identity response
        :param pulumi.Input[Union[str, 'ServiceKind']] kind: The kind of the service - e.g. "SignalR" for "Microsoft.SignalRService/SignalR"
        :param pulumi.Input[str] location: The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        :param pulumi.Input['SignalRNetworkACLsArgs'] network_acls: Network ACLs
        :param pulumi.Input[str] public_network_access: Enable or disable public network access. Default to "Enabled".
               When it's Enabled, network ACLs still apply.
               When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        :param pulumi.Input['ResourceLogConfigurationArgs'] resource_log_configuration: Resource log configuration of a Microsoft.SignalRService resource.
               If resourceLogConfiguration isn't null or empty, it will override options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
               Otherwise, use options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
        :param pulumi.Input[str] resource_name: The name of the resource.
        :param pulumi.Input['ResourceSkuArgs'] sku: The billing information of the resource.(e.g. Free, Standard)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags of the service which is a list of key value pairs that describe the resource.
        :param pulumi.Input['SignalRTlsSettingsArgs'] tls: TLS settings.
        :param pulumi.Input['ServerlessUpstreamSettingsArgs'] upstream: Upstream settings when the service is in server-less mode.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if cors is not None:
            pulumi.set(__self__, "cors", cors)
        if disable_aad_auth is None:
            disable_aad_auth = False
        if disable_aad_auth is not None:
            pulumi.set(__self__, "disable_aad_auth", disable_aad_auth)
        if disable_local_auth is None:
            disable_local_auth = False
        if disable_local_auth is not None:
            pulumi.set(__self__, "disable_local_auth", disable_local_auth)
        if features is not None:
            pulumi.set(__self__, "features", features)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_acls is not None:
            pulumi.set(__self__, "network_acls", network_acls)
        if public_network_access is None:
            public_network_access = 'Enabled'
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)
        if resource_log_configuration is not None:
            pulumi.set(__self__, "resource_log_configuration", resource_log_configuration)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tls is not None:
            pulumi.set(__self__, "tls", tls)
        if upstream is not None:
            pulumi.set(__self__, "upstream", upstream)

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
    @pulumi.getter
    def cors(self) -> Optional[pulumi.Input['SignalRCorsSettingsArgs']]:
        """
        Cross-Origin Resource Sharing (CORS) settings.
        """
        return pulumi.get(self, "cors")

    @cors.setter
    def cors(self, value: Optional[pulumi.Input['SignalRCorsSettingsArgs']]):
        pulumi.set(self, "cors", value)

    @property
    @pulumi.getter(name="disableAadAuth")
    def disable_aad_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        DisableLocalAuth
        Enable or disable aad auth
        When set as true, connection with AuthType=aad won't work.
        """
        return pulumi.get(self, "disable_aad_auth")

    @disable_aad_auth.setter
    def disable_aad_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_aad_auth", value)

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        DisableLocalAuth
        Enable or disable local auth with AccessKey
        When set as true, connection with AccessKey=xxx won't work.
        """
        return pulumi.get(self, "disable_local_auth")

    @disable_local_auth.setter
    def disable_local_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_local_auth", value)

    @property
    @pulumi.getter
    def features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SignalRFeatureArgs']]]]:
        """
        List of the featureFlags.
        
        FeatureFlags that are not included in the parameters for the update operation will not be modified.
        And the response will only include featureFlags that are explicitly set. 
        When a featureFlag is not explicitly set, its globally default value will be used
        But keep in mind, the default value doesn't mean "false". It varies in terms of different FeatureFlags.
        """
        return pulumi.get(self, "features")

    @features.setter
    def features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SignalRFeatureArgs']]]]):
        pulumi.set(self, "features", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ManagedIdentityArgs']]:
        """
        The managed identity response
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ManagedIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[Union[str, 'ServiceKind']]]:
        """
        The kind of the service - e.g. "SignalR" for "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[Union[str, 'ServiceKind']]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="networkACLs")
    def network_acls(self) -> Optional[pulumi.Input['SignalRNetworkACLsArgs']]:
        """
        Network ACLs
        """
        return pulumi.get(self, "network_acls")

    @network_acls.setter
    def network_acls(self, value: Optional[pulumi.Input['SignalRNetworkACLsArgs']]):
        pulumi.set(self, "network_acls", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[str]]:
        """
        Enable or disable public network access. Default to "Enabled".
        When it's Enabled, network ACLs still apply.
        When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_network_access", value)

    @property
    @pulumi.getter(name="resourceLogConfiguration")
    def resource_log_configuration(self) -> Optional[pulumi.Input['ResourceLogConfigurationArgs']]:
        """
        Resource log configuration of a Microsoft.SignalRService resource.
        If resourceLogConfiguration isn't null or empty, it will override options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
        Otherwise, use options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
        """
        return pulumi.get(self, "resource_log_configuration")

    @resource_log_configuration.setter
    def resource_log_configuration(self, value: Optional[pulumi.Input['ResourceLogConfigurationArgs']]):
        pulumi.set(self, "resource_log_configuration", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['ResourceSkuArgs']]:
        """
        The billing information of the resource.(e.g. Free, Standard)
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ResourceSkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags of the service which is a list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def tls(self) -> Optional[pulumi.Input['SignalRTlsSettingsArgs']]:
        """
        TLS settings.
        """
        return pulumi.get(self, "tls")

    @tls.setter
    def tls(self, value: Optional[pulumi.Input['SignalRTlsSettingsArgs']]):
        pulumi.set(self, "tls", value)

    @property
    @pulumi.getter
    def upstream(self) -> Optional[pulumi.Input['ServerlessUpstreamSettingsArgs']]:
        """
        Upstream settings when the service is in server-less mode.
        """
        return pulumi.get(self, "upstream")

    @upstream.setter
    def upstream(self, value: Optional[pulumi.Input['ServerlessUpstreamSettingsArgs']]):
        pulumi.set(self, "upstream", value)


class SignalR(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cors: Optional[pulumi.Input[pulumi.InputType['SignalRCorsSettingsArgs']]] = None,
                 disable_aad_auth: Optional[pulumi.Input[bool]] = None,
                 disable_local_auth: Optional[pulumi.Input[bool]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SignalRFeatureArgs']]]]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedIdentityArgs']]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'ServiceKind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_acls: Optional[pulumi.Input[pulumi.InputType['SignalRNetworkACLsArgs']]] = None,
                 public_network_access: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_log_configuration: Optional[pulumi.Input[pulumi.InputType['ResourceLogConfigurationArgs']]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ResourceSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tls: Optional[pulumi.Input[pulumi.InputType['SignalRTlsSettingsArgs']]] = None,
                 upstream: Optional[pulumi.Input[pulumi.InputType['ServerlessUpstreamSettingsArgs']]] = None,
                 __props__=None):
        """
        A class represent a resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SignalRCorsSettingsArgs']] cors: Cross-Origin Resource Sharing (CORS) settings.
        :param pulumi.Input[bool] disable_aad_auth: DisableLocalAuth
               Enable or disable aad auth
               When set as true, connection with AuthType=aad won't work.
        :param pulumi.Input[bool] disable_local_auth: DisableLocalAuth
               Enable or disable local auth with AccessKey
               When set as true, connection with AccessKey=xxx won't work.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SignalRFeatureArgs']]]] features: List of the featureFlags.
               
               FeatureFlags that are not included in the parameters for the update operation will not be modified.
               And the response will only include featureFlags that are explicitly set. 
               When a featureFlag is not explicitly set, its globally default value will be used
               But keep in mind, the default value doesn't mean "false". It varies in terms of different FeatureFlags.
        :param pulumi.Input[pulumi.InputType['ManagedIdentityArgs']] identity: The managed identity response
        :param pulumi.Input[Union[str, 'ServiceKind']] kind: The kind of the service - e.g. "SignalR" for "Microsoft.SignalRService/SignalR"
        :param pulumi.Input[str] location: The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        :param pulumi.Input[pulumi.InputType['SignalRNetworkACLsArgs']] network_acls: Network ACLs
        :param pulumi.Input[str] public_network_access: Enable or disable public network access. Default to "Enabled".
               When it's Enabled, network ACLs still apply.
               When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[pulumi.InputType['ResourceLogConfigurationArgs']] resource_log_configuration: Resource log configuration of a Microsoft.SignalRService resource.
               If resourceLogConfiguration isn't null or empty, it will override options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
               Otherwise, use options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
        :param pulumi.Input[str] resource_name_: The name of the resource.
        :param pulumi.Input[pulumi.InputType['ResourceSkuArgs']] sku: The billing information of the resource.(e.g. Free, Standard)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags of the service which is a list of key value pairs that describe the resource.
        :param pulumi.Input[pulumi.InputType['SignalRTlsSettingsArgs']] tls: TLS settings.
        :param pulumi.Input[pulumi.InputType['ServerlessUpstreamSettingsArgs']] upstream: Upstream settings when the service is in server-less mode.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SignalRArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A class represent a resource.

        :param str resource_name: The name of the resource.
        :param SignalRArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SignalRArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cors: Optional[pulumi.Input[pulumi.InputType['SignalRCorsSettingsArgs']]] = None,
                 disable_aad_auth: Optional[pulumi.Input[bool]] = None,
                 disable_local_auth: Optional[pulumi.Input[bool]] = None,
                 features: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SignalRFeatureArgs']]]]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedIdentityArgs']]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'ServiceKind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_acls: Optional[pulumi.Input[pulumi.InputType['SignalRNetworkACLsArgs']]] = None,
                 public_network_access: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_log_configuration: Optional[pulumi.Input[pulumi.InputType['ResourceLogConfigurationArgs']]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ResourceSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tls: Optional[pulumi.Input[pulumi.InputType['SignalRTlsSettingsArgs']]] = None,
                 upstream: Optional[pulumi.Input[pulumi.InputType['ServerlessUpstreamSettingsArgs']]] = None,
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
            __props__ = SignalRArgs.__new__(SignalRArgs)

            __props__.__dict__["cors"] = cors
            if disable_aad_auth is None:
                disable_aad_auth = False
            __props__.__dict__["disable_aad_auth"] = disable_aad_auth
            if disable_local_auth is None:
                disable_local_auth = False
            __props__.__dict__["disable_local_auth"] = disable_local_auth
            __props__.__dict__["features"] = features
            __props__.__dict__["identity"] = identity
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["network_acls"] = network_acls
            if public_network_access is None:
                public_network_access = 'Enabled'
            __props__.__dict__["public_network_access"] = public_network_access
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_log_configuration"] = resource_log_configuration
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tls"] = tls
            __props__.__dict__["upstream"] = upstream
            __props__.__dict__["external_ip"] = None
            __props__.__dict__["host_name"] = None
            __props__.__dict__["host_name_prefix"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["private_endpoint_connections"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["public_port"] = None
            __props__.__dict__["server_port"] = None
            __props__.__dict__["shared_private_link_resources"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["version"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:signalrservice:SignalR"), pulumi.Alias(type_="azure-native:signalrservice/v20180301preview:SignalR"), pulumi.Alias(type_="azure-native:signalrservice/v20181001:SignalR"), pulumi.Alias(type_="azure-native:signalrservice/v20200501:SignalR"), pulumi.Alias(type_="azure-native:signalrservice/v20200701preview:SignalR"), pulumi.Alias(type_="azure-native:signalrservice/v20210401preview:SignalR"), pulumi.Alias(type_="azure-native:signalrservice/v20210601preview:SignalR"), pulumi.Alias(type_="azure-native:signalrservice/v20210901preview:SignalR")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SignalR, __self__).__init__(
            'azure-native:signalrservice/v20211001:SignalR',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SignalR':
        """
        Get an existing SignalR resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SignalRArgs.__new__(SignalRArgs)

        __props__.__dict__["cors"] = None
        __props__.__dict__["disable_aad_auth"] = None
        __props__.__dict__["disable_local_auth"] = None
        __props__.__dict__["external_ip"] = None
        __props__.__dict__["features"] = None
        __props__.__dict__["host_name"] = None
        __props__.__dict__["host_name_prefix"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_acls"] = None
        __props__.__dict__["private_endpoint_connections"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_network_access"] = None
        __props__.__dict__["public_port"] = None
        __props__.__dict__["resource_log_configuration"] = None
        __props__.__dict__["server_port"] = None
        __props__.__dict__["shared_private_link_resources"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["tls"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["upstream"] = None
        __props__.__dict__["version"] = None
        return SignalR(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cors(self) -> pulumi.Output[Optional['outputs.SignalRCorsSettingsResponse']]:
        """
        Cross-Origin Resource Sharing (CORS) settings.
        """
        return pulumi.get(self, "cors")

    @property
    @pulumi.getter(name="disableAadAuth")
    def disable_aad_auth(self) -> pulumi.Output[Optional[bool]]:
        """
        DisableLocalAuth
        Enable or disable aad auth
        When set as true, connection with AuthType=aad won't work.
        """
        return pulumi.get(self, "disable_aad_auth")

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> pulumi.Output[Optional[bool]]:
        """
        DisableLocalAuth
        Enable or disable local auth with AccessKey
        When set as true, connection with AccessKey=xxx won't work.
        """
        return pulumi.get(self, "disable_local_auth")

    @property
    @pulumi.getter(name="externalIP")
    def external_ip(self) -> pulumi.Output[str]:
        """
        The publicly accessible IP of the resource.
        """
        return pulumi.get(self, "external_ip")

    @property
    @pulumi.getter
    def features(self) -> pulumi.Output[Optional[Sequence['outputs.SignalRFeatureResponse']]]:
        """
        List of the featureFlags.
        
        FeatureFlags that are not included in the parameters for the update operation will not be modified.
        And the response will only include featureFlags that are explicitly set. 
        When a featureFlag is not explicitly set, its globally default value will be used
        But keep in mind, the default value doesn't mean "false". It varies in terms of different FeatureFlags.
        """
        return pulumi.get(self, "features")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        FQDN of the service instance.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter(name="hostNamePrefix")
    def host_name_prefix(self) -> pulumi.Output[str]:
        """
        Deprecated.
        """
        return pulumi.get(self, "host_name_prefix")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ManagedIdentityResponse']]:
        """
        The managed identity response
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        The kind of the service - e.g. "SignalR" for "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The GEO location of the resource. e.g. West US | East US | North Central US | South Central US.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkACLs")
    def network_acls(self) -> pulumi.Output[Optional['outputs.SignalRNetworkACLsResponse']]:
        """
        Network ACLs
        """
        return pulumi.get(self, "network_acls")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        Private endpoint connections to the resource.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> pulumi.Output[Optional[str]]:
        """
        Enable or disable public network access. Default to "Enabled".
        When it's Enabled, network ACLs still apply.
        When it's Disabled, public network access is always disabled no matter what you set in network ACLs.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="publicPort")
    def public_port(self) -> pulumi.Output[int]:
        """
        The publicly accessible port of the resource which is designed for browser/client side usage.
        """
        return pulumi.get(self, "public_port")

    @property
    @pulumi.getter(name="resourceLogConfiguration")
    def resource_log_configuration(self) -> pulumi.Output[Optional['outputs.ResourceLogConfigurationResponse']]:
        """
        Resource log configuration of a Microsoft.SignalRService resource.
        If resourceLogConfiguration isn't null or empty, it will override options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
        Otherwise, use options "EnableConnectivityLog" and "EnableMessagingLogs" in features.
        """
        return pulumi.get(self, "resource_log_configuration")

    @property
    @pulumi.getter(name="serverPort")
    def server_port(self) -> pulumi.Output[int]:
        """
        The publicly accessible port of the resource which is designed for customer server side usage.
        """
        return pulumi.get(self, "server_port")

    @property
    @pulumi.getter(name="sharedPrivateLinkResources")
    def shared_private_link_resources(self) -> pulumi.Output[Sequence['outputs.SharedPrivateLinkResourceResponse']]:
        """
        The list of shared private link resources.
        """
        return pulumi.get(self, "shared_private_link_resources")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ResourceSkuResponse']]:
        """
        The billing information of the resource.(e.g. Free, Standard)
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags of the service which is a list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def tls(self) -> pulumi.Output[Optional['outputs.SignalRTlsSettingsResponse']]:
        """
        TLS settings.
        """
        return pulumi.get(self, "tls")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource - e.g. "Microsoft.SignalRService/SignalR"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def upstream(self) -> pulumi.Output[Optional['outputs.ServerlessUpstreamSettingsResponse']]:
        """
        Upstream settings when the service is in server-less mode.
        """
        return pulumi.get(self, "upstream")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[str]:
        """
        Version of the resource. Probably you need the same or higher version of client SDKs.
        """
        return pulumi.get(self, "version")

