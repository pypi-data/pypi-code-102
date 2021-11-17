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

__all__ = ['ManagedClusterArgs', 'ManagedCluster']

@pulumi.input_type
class ManagedClusterArgs:
    def __init__(__self__, *,
                 admin_user_name: pulumi.Input[str],
                 dns_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 addon_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 admin_password: Optional[pulumi.Input[str]] = None,
                 azure_active_directory: Optional[pulumi.Input['AzureActiveDirectoryArgs']] = None,
                 client_connection_port: Optional[pulumi.Input[int]] = None,
                 clients: Optional[pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]]] = None,
                 cluster_code_version: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 fabric_settings: Optional[pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]]] = None,
                 http_gateway_connection_port: Optional[pulumi.Input[int]] = None,
                 load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['SkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ManagedCluster resource.
        :param pulumi.Input[str] admin_user_name: vm admin user name.
        :param pulumi.Input[str] dns_name: The cluster dns name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] addon_features: client certificates for the cluster.
        :param pulumi.Input[str] admin_password: vm admin user password.
        :param pulumi.Input['AzureActiveDirectoryArgs'] azure_active_directory: Azure active directory.
        :param pulumi.Input[int] client_connection_port: The port used for client connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]] clients: client certificates for the cluster.
        :param pulumi.Input[str] cluster_code_version: The Service Fabric runtime version of the cluster. This property can only by set the user when **upgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        :param pulumi.Input[str] cluster_name: The name of the cluster resource.
        :param pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]] fabric_settings: The list of custom fabric settings to configure the cluster.
        :param pulumi.Input[int] http_gateway_connection_port: The port used for http connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]] load_balancing_rules: Describes load balancing rules.
        :param pulumi.Input[str] location: Azure resource location.
        :param pulumi.Input['SkuArgs'] sku: The sku of the managed cluster
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Azure resource tags.
        """
        pulumi.set(__self__, "admin_user_name", admin_user_name)
        pulumi.set(__self__, "dns_name", dns_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if addon_features is not None:
            pulumi.set(__self__, "addon_features", addon_features)
        if admin_password is not None:
            pulumi.set(__self__, "admin_password", admin_password)
        if azure_active_directory is not None:
            pulumi.set(__self__, "azure_active_directory", azure_active_directory)
        if client_connection_port is None:
            client_connection_port = 19000
        if client_connection_port is not None:
            pulumi.set(__self__, "client_connection_port", client_connection_port)
        if clients is not None:
            pulumi.set(__self__, "clients", clients)
        if cluster_code_version is not None:
            pulumi.set(__self__, "cluster_code_version", cluster_code_version)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if fabric_settings is not None:
            pulumi.set(__self__, "fabric_settings", fabric_settings)
        if http_gateway_connection_port is None:
            http_gateway_connection_port = 19080
        if http_gateway_connection_port is not None:
            pulumi.set(__self__, "http_gateway_connection_port", http_gateway_connection_port)
        if load_balancing_rules is not None:
            pulumi.set(__self__, "load_balancing_rules", load_balancing_rules)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="adminUserName")
    def admin_user_name(self) -> pulumi.Input[str]:
        """
        vm admin user name.
        """
        return pulumi.get(self, "admin_user_name")

    @admin_user_name.setter
    def admin_user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "admin_user_name", value)

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> pulumi.Input[str]:
        """
        The cluster dns name.
        """
        return pulumi.get(self, "dns_name")

    @dns_name.setter
    def dns_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "dns_name", value)

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
    @pulumi.getter(name="addonFeatures")
    def addon_features(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        client certificates for the cluster.
        """
        return pulumi.get(self, "addon_features")

    @addon_features.setter
    def addon_features(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "addon_features", value)

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> Optional[pulumi.Input[str]]:
        """
        vm admin user password.
        """
        return pulumi.get(self, "admin_password")

    @admin_password.setter
    def admin_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "admin_password", value)

    @property
    @pulumi.getter(name="azureActiveDirectory")
    def azure_active_directory(self) -> Optional[pulumi.Input['AzureActiveDirectoryArgs']]:
        """
        Azure active directory.
        """
        return pulumi.get(self, "azure_active_directory")

    @azure_active_directory.setter
    def azure_active_directory(self, value: Optional[pulumi.Input['AzureActiveDirectoryArgs']]):
        pulumi.set(self, "azure_active_directory", value)

    @property
    @pulumi.getter(name="clientConnectionPort")
    def client_connection_port(self) -> Optional[pulumi.Input[int]]:
        """
        The port used for client connections to the cluster.
        """
        return pulumi.get(self, "client_connection_port")

    @client_connection_port.setter
    def client_connection_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "client_connection_port", value)

    @property
    @pulumi.getter
    def clients(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]]]:
        """
        client certificates for the cluster.
        """
        return pulumi.get(self, "clients")

    @clients.setter
    def clients(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClientCertificateArgs']]]]):
        pulumi.set(self, "clients", value)

    @property
    @pulumi.getter(name="clusterCodeVersion")
    def cluster_code_version(self) -> Optional[pulumi.Input[str]]:
        """
        The Service Fabric runtime version of the cluster. This property can only by set the user when **upgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        """
        return pulumi.get(self, "cluster_code_version")

    @cluster_code_version.setter
    def cluster_code_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_code_version", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the cluster resource.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="fabricSettings")
    def fabric_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]]]:
        """
        The list of custom fabric settings to configure the cluster.
        """
        return pulumi.get(self, "fabric_settings")

    @fabric_settings.setter
    def fabric_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SettingsSectionDescriptionArgs']]]]):
        pulumi.set(self, "fabric_settings", value)

    @property
    @pulumi.getter(name="httpGatewayConnectionPort")
    def http_gateway_connection_port(self) -> Optional[pulumi.Input[int]]:
        """
        The port used for http connections to the cluster.
        """
        return pulumi.get(self, "http_gateway_connection_port")

    @http_gateway_connection_port.setter
    def http_gateway_connection_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "http_gateway_connection_port", value)

    @property
    @pulumi.getter(name="loadBalancingRules")
    def load_balancing_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]]:
        """
        Describes load balancing rules.
        """
        return pulumi.get(self, "load_balancing_rules")

    @load_balancing_rules.setter
    def load_balancing_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LoadBalancingRuleArgs']]]]):
        pulumi.set(self, "load_balancing_rules", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Azure resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        The sku of the managed cluster
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Azure resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class ManagedCluster(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 addon_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 admin_password: Optional[pulumi.Input[str]] = None,
                 admin_user_name: Optional[pulumi.Input[str]] = None,
                 azure_active_directory: Optional[pulumi.Input[pulumi.InputType['AzureActiveDirectoryArgs']]] = None,
                 client_connection_port: Optional[pulumi.Input[int]] = None,
                 clients: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientCertificateArgs']]]]] = None,
                 cluster_code_version: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 dns_name: Optional[pulumi.Input[str]] = None,
                 fabric_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SettingsSectionDescriptionArgs']]]]] = None,
                 http_gateway_connection_port: Optional[pulumi.Input[int]] = None,
                 load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The manged cluster resource

        API Version: 2020-01-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] addon_features: client certificates for the cluster.
        :param pulumi.Input[str] admin_password: vm admin user password.
        :param pulumi.Input[str] admin_user_name: vm admin user name.
        :param pulumi.Input[pulumi.InputType['AzureActiveDirectoryArgs']] azure_active_directory: Azure active directory.
        :param pulumi.Input[int] client_connection_port: The port used for client connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientCertificateArgs']]]] clients: client certificates for the cluster.
        :param pulumi.Input[str] cluster_code_version: The Service Fabric runtime version of the cluster. This property can only by set the user when **upgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        :param pulumi.Input[str] cluster_name: The name of the cluster resource.
        :param pulumi.Input[str] dns_name: The cluster dns name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SettingsSectionDescriptionArgs']]]] fabric_settings: The list of custom fabric settings to configure the cluster.
        :param pulumi.Input[int] http_gateway_connection_port: The port used for http connections to the cluster.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]] load_balancing_rules: Describes load balancing rules.
        :param pulumi.Input[str] location: Azure resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku of the managed cluster
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Azure resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The manged cluster resource

        API Version: 2020-01-01-preview.

        :param str resource_name: The name of the resource.
        :param ManagedClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 addon_features: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 admin_password: Optional[pulumi.Input[str]] = None,
                 admin_user_name: Optional[pulumi.Input[str]] = None,
                 azure_active_directory: Optional[pulumi.Input[pulumi.InputType['AzureActiveDirectoryArgs']]] = None,
                 client_connection_port: Optional[pulumi.Input[int]] = None,
                 clients: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientCertificateArgs']]]]] = None,
                 cluster_code_version: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 dns_name: Optional[pulumi.Input[str]] = None,
                 fabric_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SettingsSectionDescriptionArgs']]]]] = None,
                 http_gateway_connection_port: Optional[pulumi.Input[int]] = None,
                 load_balancing_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LoadBalancingRuleArgs']]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
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
            __props__ = ManagedClusterArgs.__new__(ManagedClusterArgs)

            __props__.__dict__["addon_features"] = addon_features
            __props__.__dict__["admin_password"] = admin_password
            if admin_user_name is None and not opts.urn:
                raise TypeError("Missing required property 'admin_user_name'")
            __props__.__dict__["admin_user_name"] = admin_user_name
            __props__.__dict__["azure_active_directory"] = azure_active_directory
            if client_connection_port is None:
                client_connection_port = 19000
            __props__.__dict__["client_connection_port"] = client_connection_port
            __props__.__dict__["clients"] = clients
            __props__.__dict__["cluster_code_version"] = cluster_code_version
            __props__.__dict__["cluster_name"] = cluster_name
            if dns_name is None and not opts.urn:
                raise TypeError("Missing required property 'dns_name'")
            __props__.__dict__["dns_name"] = dns_name
            __props__.__dict__["fabric_settings"] = fabric_settings
            if http_gateway_connection_port is None:
                http_gateway_connection_port = 19080
            __props__.__dict__["http_gateway_connection_port"] = http_gateway_connection_port
            __props__.__dict__["load_balancing_rules"] = load_balancing_rules
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["cluster_certificate_thumbprint"] = None
            __props__.__dict__["cluster_id"] = None
            __props__.__dict__["cluster_state"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["fqdn"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:servicefabric/v20200101preview:ManagedCluster"), pulumi.Alias(type_="azure-native:servicefabric/v20210101preview:ManagedCluster"), pulumi.Alias(type_="azure-native:servicefabric/v20210501:ManagedCluster"), pulumi.Alias(type_="azure-native:servicefabric/v20210701preview:ManagedCluster"), pulumi.Alias(type_="azure-native:servicefabric/v20210901privatepreview:ManagedCluster"), pulumi.Alias(type_="azure-native:servicefabric/v20211101preview:ManagedCluster")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedCluster, __self__).__init__(
            'azure-native:servicefabric:ManagedCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedCluster':
        """
        Get an existing ManagedCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ManagedClusterArgs.__new__(ManagedClusterArgs)

        __props__.__dict__["addon_features"] = None
        __props__.__dict__["admin_password"] = None
        __props__.__dict__["admin_user_name"] = None
        __props__.__dict__["azure_active_directory"] = None
        __props__.__dict__["client_connection_port"] = None
        __props__.__dict__["clients"] = None
        __props__.__dict__["cluster_certificate_thumbprint"] = None
        __props__.__dict__["cluster_code_version"] = None
        __props__.__dict__["cluster_id"] = None
        __props__.__dict__["cluster_state"] = None
        __props__.__dict__["dns_name"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["fabric_settings"] = None
        __props__.__dict__["fqdn"] = None
        __props__.__dict__["http_gateway_connection_port"] = None
        __props__.__dict__["load_balancing_rules"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ManagedCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addonFeatures")
    def addon_features(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        client certificates for the cluster.
        """
        return pulumi.get(self, "addon_features")

    @property
    @pulumi.getter(name="adminPassword")
    def admin_password(self) -> pulumi.Output[Optional[str]]:
        """
        vm admin user password.
        """
        return pulumi.get(self, "admin_password")

    @property
    @pulumi.getter(name="adminUserName")
    def admin_user_name(self) -> pulumi.Output[str]:
        """
        vm admin user name.
        """
        return pulumi.get(self, "admin_user_name")

    @property
    @pulumi.getter(name="azureActiveDirectory")
    def azure_active_directory(self) -> pulumi.Output[Optional['outputs.AzureActiveDirectoryResponse']]:
        """
        Azure active directory.
        """
        return pulumi.get(self, "azure_active_directory")

    @property
    @pulumi.getter(name="clientConnectionPort")
    def client_connection_port(self) -> pulumi.Output[Optional[int]]:
        """
        The port used for client connections to the cluster.
        """
        return pulumi.get(self, "client_connection_port")

    @property
    @pulumi.getter
    def clients(self) -> pulumi.Output[Optional[Sequence['outputs.ClientCertificateResponse']]]:
        """
        client certificates for the cluster.
        """
        return pulumi.get(self, "clients")

    @property
    @pulumi.getter(name="clusterCertificateThumbprint")
    def cluster_certificate_thumbprint(self) -> pulumi.Output[str]:
        """
        The cluster certificate thumbprint used node to node communication.
        """
        return pulumi.get(self, "cluster_certificate_thumbprint")

    @property
    @pulumi.getter(name="clusterCodeVersion")
    def cluster_code_version(self) -> pulumi.Output[Optional[str]]:
        """
        The Service Fabric runtime version of the cluster. This property can only by set the user when **upgradeMode** is set to 'Manual'. To get list of available Service Fabric versions for new clusters use [ClusterVersion API](./ClusterVersion.md). To get the list of available version for existing clusters use **availableClusterVersions**.
        """
        return pulumi.get(self, "cluster_code_version")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Output[str]:
        """
        A service generated unique identifier for the cluster resource.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="clusterState")
    def cluster_state(self) -> pulumi.Output[str]:
        """
        The current state of the cluster.
        """
        return pulumi.get(self, "cluster_state")

    @property
    @pulumi.getter(name="dnsName")
    def dns_name(self) -> pulumi.Output[str]:
        """
        The cluster dns name.
        """
        return pulumi.get(self, "dns_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Azure resource etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="fabricSettings")
    def fabric_settings(self) -> pulumi.Output[Optional[Sequence['outputs.SettingsSectionDescriptionResponse']]]:
        """
        The list of custom fabric settings to configure the cluster.
        """
        return pulumi.get(self, "fabric_settings")

    @property
    @pulumi.getter
    def fqdn(self) -> pulumi.Output[str]:
        """
        the cluster Fully qualified domain name.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="httpGatewayConnectionPort")
    def http_gateway_connection_port(self) -> pulumi.Output[Optional[int]]:
        """
        The port used for http connections to the cluster.
        """
        return pulumi.get(self, "http_gateway_connection_port")

    @property
    @pulumi.getter(name="loadBalancingRules")
    def load_balancing_rules(self) -> pulumi.Output[Optional[Sequence['outputs.LoadBalancingRuleResponse']]]:
        """
        Describes load balancing rules.
        """
        return pulumi.get(self, "load_balancing_rules")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Azure resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the managed cluster resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of the managed cluster
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Azure resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type.
        """
        return pulumi.get(self, "type")

