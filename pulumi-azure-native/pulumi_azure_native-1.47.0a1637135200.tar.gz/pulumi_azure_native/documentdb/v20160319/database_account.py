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

__all__ = ['DatabaseAccountArgs', 'DatabaseAccount']

@pulumi.input_type
class DatabaseAccountArgs:
    def __init__(__self__, *,
                 database_account_offer_type: pulumi.Input['DatabaseAccountOfferType'],
                 locations: pulumi.Input[Sequence[pulumi.Input['LocationArgs']]],
                 resource_group_name: pulumi.Input[str],
                 account_name: Optional[pulumi.Input[str]] = None,
                 capabilities: Optional[pulumi.Input[Sequence[pulumi.Input['CapabilityArgs']]]] = None,
                 connector_offer: Optional[pulumi.Input[Union[str, 'ConnectorOffer']]] = None,
                 consistency_policy: Optional[pulumi.Input['ConsistencyPolicyArgs']] = None,
                 enable_automatic_failover: Optional[pulumi.Input[bool]] = None,
                 enable_cassandra_connector: Optional[pulumi.Input[bool]] = None,
                 enable_multiple_write_locations: Optional[pulumi.Input[bool]] = None,
                 ip_range_filter: Optional[pulumi.Input[str]] = None,
                 is_virtual_network_filter_enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'DatabaseAccountKind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_network_rules: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]] = None):
        """
        The set of arguments for constructing a DatabaseAccount resource.
        :param pulumi.Input['DatabaseAccountOfferType'] database_account_offer_type: The offer type for the database
        :param pulumi.Input[Sequence[pulumi.Input['LocationArgs']]] locations: An array that contains the georeplication locations enabled for the Cosmos DB account.
        :param pulumi.Input[str] resource_group_name: Name of an Azure resource group.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[Sequence[pulumi.Input['CapabilityArgs']]] capabilities: List of Cosmos DB capabilities for the account
        :param pulumi.Input[Union[str, 'ConnectorOffer']] connector_offer: The cassandra connector offer type for the Cosmos DB database C* account.
        :param pulumi.Input['ConsistencyPolicyArgs'] consistency_policy: The consistency policy for the Cosmos DB account.
        :param pulumi.Input[bool] enable_automatic_failover: Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
        :param pulumi.Input[bool] enable_cassandra_connector: Enables the cassandra connector on the Cosmos DB C* account
        :param pulumi.Input[bool] enable_multiple_write_locations: Enables the account to write in multiple locations
        :param pulumi.Input[str] ip_range_filter: Cosmos DB Firewall Support: This value specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma separated and must not contain any spaces.
        :param pulumi.Input[bool] is_virtual_network_filter_enabled: Flag to indicate whether to enable/disable Virtual Network ACL rules.
        :param pulumi.Input[Union[str, 'DatabaseAccountKind']] kind: Indicates the type of database account. This can only be set at database account creation.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        :param pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]] virtual_network_rules: List of Virtual Network ACL rules configured for the Cosmos DB account.
        """
        pulumi.set(__self__, "database_account_offer_type", database_account_offer_type)
        pulumi.set(__self__, "locations", locations)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if capabilities is not None:
            pulumi.set(__self__, "capabilities", capabilities)
        if connector_offer is not None:
            pulumi.set(__self__, "connector_offer", connector_offer)
        if consistency_policy is not None:
            pulumi.set(__self__, "consistency_policy", consistency_policy)
        if enable_automatic_failover is not None:
            pulumi.set(__self__, "enable_automatic_failover", enable_automatic_failover)
        if enable_cassandra_connector is not None:
            pulumi.set(__self__, "enable_cassandra_connector", enable_cassandra_connector)
        if enable_multiple_write_locations is not None:
            pulumi.set(__self__, "enable_multiple_write_locations", enable_multiple_write_locations)
        if ip_range_filter is not None:
            pulumi.set(__self__, "ip_range_filter", ip_range_filter)
        if is_virtual_network_filter_enabled is not None:
            pulumi.set(__self__, "is_virtual_network_filter_enabled", is_virtual_network_filter_enabled)
        if kind is None:
            kind = 'GlobalDocumentDB'
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if virtual_network_rules is not None:
            pulumi.set(__self__, "virtual_network_rules", virtual_network_rules)

    @property
    @pulumi.getter(name="databaseAccountOfferType")
    def database_account_offer_type(self) -> pulumi.Input['DatabaseAccountOfferType']:
        """
        The offer type for the database
        """
        return pulumi.get(self, "database_account_offer_type")

    @database_account_offer_type.setter
    def database_account_offer_type(self, value: pulumi.Input['DatabaseAccountOfferType']):
        pulumi.set(self, "database_account_offer_type", value)

    @property
    @pulumi.getter
    def locations(self) -> pulumi.Input[Sequence[pulumi.Input['LocationArgs']]]:
        """
        An array that contains the georeplication locations enabled for the Cosmos DB account.
        """
        return pulumi.get(self, "locations")

    @locations.setter
    def locations(self, value: pulumi.Input[Sequence[pulumi.Input['LocationArgs']]]):
        pulumi.set(self, "locations", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of an Azure resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        Cosmos DB database account name.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def capabilities(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CapabilityArgs']]]]:
        """
        List of Cosmos DB capabilities for the account
        """
        return pulumi.get(self, "capabilities")

    @capabilities.setter
    def capabilities(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CapabilityArgs']]]]):
        pulumi.set(self, "capabilities", value)

    @property
    @pulumi.getter(name="connectorOffer")
    def connector_offer(self) -> Optional[pulumi.Input[Union[str, 'ConnectorOffer']]]:
        """
        The cassandra connector offer type for the Cosmos DB database C* account.
        """
        return pulumi.get(self, "connector_offer")

    @connector_offer.setter
    def connector_offer(self, value: Optional[pulumi.Input[Union[str, 'ConnectorOffer']]]):
        pulumi.set(self, "connector_offer", value)

    @property
    @pulumi.getter(name="consistencyPolicy")
    def consistency_policy(self) -> Optional[pulumi.Input['ConsistencyPolicyArgs']]:
        """
        The consistency policy for the Cosmos DB account.
        """
        return pulumi.get(self, "consistency_policy")

    @consistency_policy.setter
    def consistency_policy(self, value: Optional[pulumi.Input['ConsistencyPolicyArgs']]):
        pulumi.set(self, "consistency_policy", value)

    @property
    @pulumi.getter(name="enableAutomaticFailover")
    def enable_automatic_failover(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
        """
        return pulumi.get(self, "enable_automatic_failover")

    @enable_automatic_failover.setter
    def enable_automatic_failover(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_automatic_failover", value)

    @property
    @pulumi.getter(name="enableCassandraConnector")
    def enable_cassandra_connector(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables the cassandra connector on the Cosmos DB C* account
        """
        return pulumi.get(self, "enable_cassandra_connector")

    @enable_cassandra_connector.setter
    def enable_cassandra_connector(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_cassandra_connector", value)

    @property
    @pulumi.getter(name="enableMultipleWriteLocations")
    def enable_multiple_write_locations(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables the account to write in multiple locations
        """
        return pulumi.get(self, "enable_multiple_write_locations")

    @enable_multiple_write_locations.setter
    def enable_multiple_write_locations(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_multiple_write_locations", value)

    @property
    @pulumi.getter(name="ipRangeFilter")
    def ip_range_filter(self) -> Optional[pulumi.Input[str]]:
        """
        Cosmos DB Firewall Support: This value specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma separated and must not contain any spaces.
        """
        return pulumi.get(self, "ip_range_filter")

    @ip_range_filter.setter
    def ip_range_filter(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_range_filter", value)

    @property
    @pulumi.getter(name="isVirtualNetworkFilterEnabled")
    def is_virtual_network_filter_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag to indicate whether to enable/disable Virtual Network ACL rules.
        """
        return pulumi.get(self, "is_virtual_network_filter_enabled")

    @is_virtual_network_filter_enabled.setter
    def is_virtual_network_filter_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_virtual_network_filter_enabled", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[Union[str, 'DatabaseAccountKind']]]:
        """
        Indicates the type of database account. This can only be set at database account creation.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[Union[str, 'DatabaseAccountKind']]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]]:
        """
        List of Virtual Network ACL rules configured for the Cosmos DB account.
        """
        return pulumi.get(self, "virtual_network_rules")

    @virtual_network_rules.setter
    def virtual_network_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VirtualNetworkRuleArgs']]]]):
        pulumi.set(self, "virtual_network_rules", value)


class DatabaseAccount(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 capabilities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CapabilityArgs']]]]] = None,
                 connector_offer: Optional[pulumi.Input[Union[str, 'ConnectorOffer']]] = None,
                 consistency_policy: Optional[pulumi.Input[pulumi.InputType['ConsistencyPolicyArgs']]] = None,
                 database_account_offer_type: Optional[pulumi.Input['DatabaseAccountOfferType']] = None,
                 enable_automatic_failover: Optional[pulumi.Input[bool]] = None,
                 enable_cassandra_connector: Optional[pulumi.Input[bool]] = None,
                 enable_multiple_write_locations: Optional[pulumi.Input[bool]] = None,
                 ip_range_filter: Optional[pulumi.Input[str]] = None,
                 is_virtual_network_filter_enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'DatabaseAccountKind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 locations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LocationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_network_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualNetworkRuleArgs']]]]] = None,
                 __props__=None):
        """
        An Azure Cosmos DB database account.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CapabilityArgs']]]] capabilities: List of Cosmos DB capabilities for the account
        :param pulumi.Input[Union[str, 'ConnectorOffer']] connector_offer: The cassandra connector offer type for the Cosmos DB database C* account.
        :param pulumi.Input[pulumi.InputType['ConsistencyPolicyArgs']] consistency_policy: The consistency policy for the Cosmos DB account.
        :param pulumi.Input['DatabaseAccountOfferType'] database_account_offer_type: The offer type for the database
        :param pulumi.Input[bool] enable_automatic_failover: Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
        :param pulumi.Input[bool] enable_cassandra_connector: Enables the cassandra connector on the Cosmos DB C* account
        :param pulumi.Input[bool] enable_multiple_write_locations: Enables the account to write in multiple locations
        :param pulumi.Input[str] ip_range_filter: Cosmos DB Firewall Support: This value specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma separated and must not contain any spaces.
        :param pulumi.Input[bool] is_virtual_network_filter_enabled: Flag to indicate whether to enable/disable Virtual Network ACL rules.
        :param pulumi.Input[Union[str, 'DatabaseAccountKind']] kind: Indicates the type of database account. This can only be set at database account creation.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LocationArgs']]]] locations: An array that contains the georeplication locations enabled for the Cosmos DB account.
        :param pulumi.Input[str] resource_group_name: Name of an Azure resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualNetworkRuleArgs']]]] virtual_network_rules: List of Virtual Network ACL rules configured for the Cosmos DB account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatabaseAccountArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Azure Cosmos DB database account.

        :param str resource_name: The name of the resource.
        :param DatabaseAccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseAccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 capabilities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CapabilityArgs']]]]] = None,
                 connector_offer: Optional[pulumi.Input[Union[str, 'ConnectorOffer']]] = None,
                 consistency_policy: Optional[pulumi.Input[pulumi.InputType['ConsistencyPolicyArgs']]] = None,
                 database_account_offer_type: Optional[pulumi.Input['DatabaseAccountOfferType']] = None,
                 enable_automatic_failover: Optional[pulumi.Input[bool]] = None,
                 enable_cassandra_connector: Optional[pulumi.Input[bool]] = None,
                 enable_multiple_write_locations: Optional[pulumi.Input[bool]] = None,
                 ip_range_filter: Optional[pulumi.Input[str]] = None,
                 is_virtual_network_filter_enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'DatabaseAccountKind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 locations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LocationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_network_rules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualNetworkRuleArgs']]]]] = None,
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
            __props__ = DatabaseAccountArgs.__new__(DatabaseAccountArgs)

            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["capabilities"] = capabilities
            __props__.__dict__["connector_offer"] = connector_offer
            __props__.__dict__["consistency_policy"] = consistency_policy
            if database_account_offer_type is None and not opts.urn:
                raise TypeError("Missing required property 'database_account_offer_type'")
            __props__.__dict__["database_account_offer_type"] = database_account_offer_type
            __props__.__dict__["enable_automatic_failover"] = enable_automatic_failover
            __props__.__dict__["enable_cassandra_connector"] = enable_cassandra_connector
            __props__.__dict__["enable_multiple_write_locations"] = enable_multiple_write_locations
            __props__.__dict__["ip_range_filter"] = ip_range_filter
            __props__.__dict__["is_virtual_network_filter_enabled"] = is_virtual_network_filter_enabled
            if kind is None:
                kind = 'GlobalDocumentDB'
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            if locations is None and not opts.urn:
                raise TypeError("Missing required property 'locations'")
            __props__.__dict__["locations"] = locations
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["virtual_network_rules"] = virtual_network_rules
            __props__.__dict__["document_endpoint"] = None
            __props__.__dict__["failover_policies"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["read_locations"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["write_locations"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:documentdb:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20150401:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20150408:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20151106:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20160331:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20190801:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20191212:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20200301:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20200401:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20200601preview:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20200901:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210115:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210301preview:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210315:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210401preview:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210415:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210515:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210615:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20210701preview:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20211015:DatabaseAccount"), pulumi.Alias(type_="azure-native:documentdb/v20211015preview:DatabaseAccount")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DatabaseAccount, __self__).__init__(
            'azure-native:documentdb/v20160319:DatabaseAccount',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DatabaseAccount':
        """
        Get an existing DatabaseAccount resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DatabaseAccountArgs.__new__(DatabaseAccountArgs)

        __props__.__dict__["capabilities"] = None
        __props__.__dict__["connector_offer"] = None
        __props__.__dict__["consistency_policy"] = None
        __props__.__dict__["database_account_offer_type"] = None
        __props__.__dict__["document_endpoint"] = None
        __props__.__dict__["enable_automatic_failover"] = None
        __props__.__dict__["enable_cassandra_connector"] = None
        __props__.__dict__["enable_multiple_write_locations"] = None
        __props__.__dict__["failover_policies"] = None
        __props__.__dict__["ip_range_filter"] = None
        __props__.__dict__["is_virtual_network_filter_enabled"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["read_locations"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["virtual_network_rules"] = None
        __props__.__dict__["write_locations"] = None
        return DatabaseAccount(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def capabilities(self) -> pulumi.Output[Optional[Sequence['outputs.CapabilityResponse']]]:
        """
        List of Cosmos DB capabilities for the account
        """
        return pulumi.get(self, "capabilities")

    @property
    @pulumi.getter(name="connectorOffer")
    def connector_offer(self) -> pulumi.Output[Optional[str]]:
        """
        The cassandra connector offer type for the Cosmos DB database C* account.
        """
        return pulumi.get(self, "connector_offer")

    @property
    @pulumi.getter(name="consistencyPolicy")
    def consistency_policy(self) -> pulumi.Output[Optional['outputs.ConsistencyPolicyResponse']]:
        """
        The consistency policy for the Cosmos DB database account.
        """
        return pulumi.get(self, "consistency_policy")

    @property
    @pulumi.getter(name="databaseAccountOfferType")
    def database_account_offer_type(self) -> pulumi.Output[str]:
        """
        The offer type for the Cosmos DB database account. Default value: Standard.
        """
        return pulumi.get(self, "database_account_offer_type")

    @property
    @pulumi.getter(name="documentEndpoint")
    def document_endpoint(self) -> pulumi.Output[str]:
        """
        The connection endpoint for the Cosmos DB database account.
        """
        return pulumi.get(self, "document_endpoint")

    @property
    @pulumi.getter(name="enableAutomaticFailover")
    def enable_automatic_failover(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables automatic failover of the write region in the rare event that the region is unavailable due to an outage. Automatic failover will result in a new write region for the account and is chosen based on the failover priorities configured for the account.
        """
        return pulumi.get(self, "enable_automatic_failover")

    @property
    @pulumi.getter(name="enableCassandraConnector")
    def enable_cassandra_connector(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables the cassandra connector on the Cosmos DB C* account
        """
        return pulumi.get(self, "enable_cassandra_connector")

    @property
    @pulumi.getter(name="enableMultipleWriteLocations")
    def enable_multiple_write_locations(self) -> pulumi.Output[Optional[bool]]:
        """
        Enables the account to write in multiple locations
        """
        return pulumi.get(self, "enable_multiple_write_locations")

    @property
    @pulumi.getter(name="failoverPolicies")
    def failover_policies(self) -> pulumi.Output[Sequence['outputs.FailoverPolicyResponse']]:
        """
        An array that contains the regions ordered by their failover priorities.
        """
        return pulumi.get(self, "failover_policies")

    @property
    @pulumi.getter(name="ipRangeFilter")
    def ip_range_filter(self) -> pulumi.Output[Optional[str]]:
        """
        Cosmos DB Firewall Support: This value specifies the set of IP addresses or IP address ranges in CIDR form to be included as the allowed list of client IPs for a given database account. IP addresses/ranges must be comma separated and must not contain any spaces.
        """
        return pulumi.get(self, "ip_range_filter")

    @property
    @pulumi.getter(name="isVirtualNetworkFilterEnabled")
    def is_virtual_network_filter_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag to indicate whether to enable/disable Virtual Network ACL rules.
        """
        return pulumi.get(self, "is_virtual_network_filter_enabled")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the type of database account. This can only be set at database account creation.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the database account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The status of the Cosmos DB account at the time the operation was called. The status can be one of following. 'Creating' – the Cosmos DB account is being created. When an account is in Creating state, only properties that are specified as input for the Create Cosmos DB account operation are returned. 'Succeeded' – the Cosmos DB account is active for use. 'Updating' – the Cosmos DB account is being updated. 'Deleting' – the Cosmos DB account is being deleted. 'Failed' – the Cosmos DB account failed creation. 'Offline' - the Cosmos DB account is not active. 'DeletionFailed' – the Cosmos DB account deletion failed.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="readLocations")
    def read_locations(self) -> pulumi.Output[Sequence['outputs.LocationResponse']]:
        """
        An array that contains of the read locations enabled for the Cosmos DB account.
        """
        return pulumi.get(self, "read_locations")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualNetworkRules")
    def virtual_network_rules(self) -> pulumi.Output[Optional[Sequence['outputs.VirtualNetworkRuleResponse']]]:
        """
        List of Virtual Network ACL rules configured for the Cosmos DB account.
        """
        return pulumi.get(self, "virtual_network_rules")

    @property
    @pulumi.getter(name="writeLocations")
    def write_locations(self) -> pulumi.Output[Sequence['outputs.LocationResponse']]:
        """
        An array that contains the write location for the Cosmos DB account.
        """
        return pulumi.get(self, "write_locations")

