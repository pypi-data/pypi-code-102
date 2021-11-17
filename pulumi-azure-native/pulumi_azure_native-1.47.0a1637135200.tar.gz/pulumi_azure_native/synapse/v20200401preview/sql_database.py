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

__all__ = ['SqlDatabaseArgs', 'SqlDatabase']

@pulumi.input_type
class SqlDatabaseArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 collation: Optional[pulumi.Input[str]] = None,
                 data_retention: Optional[pulumi.Input['SqlDatabaseDataRetentionArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 sql_database_name: Optional[pulumi.Input[str]] = None,
                 storage_redundancy: Optional[pulumi.Input[Union[str, 'StorageRedundancy']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a SqlDatabase resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] collation: The collation of the database.
        :param pulumi.Input['SqlDatabaseDataRetentionArgs'] data_retention: Sql database data retention.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] sql_database_name: The name of the sql database.
        :param pulumi.Input[Union[str, 'StorageRedundancy']] storage_redundancy: The storage redundancy of the database.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if collation is not None:
            pulumi.set(__self__, "collation", collation)
        if data_retention is not None:
            pulumi.set(__self__, "data_retention", data_retention)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if sql_database_name is not None:
            pulumi.set(__self__, "sql_database_name", sql_database_name)
        if storage_redundancy is not None:
            pulumi.set(__self__, "storage_redundancy", storage_redundancy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

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
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter
    def collation(self) -> Optional[pulumi.Input[str]]:
        """
        The collation of the database.
        """
        return pulumi.get(self, "collation")

    @collation.setter
    def collation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "collation", value)

    @property
    @pulumi.getter(name="dataRetention")
    def data_retention(self) -> Optional[pulumi.Input['SqlDatabaseDataRetentionArgs']]:
        """
        Sql database data retention.
        """
        return pulumi.get(self, "data_retention")

    @data_retention.setter
    def data_retention(self, value: Optional[pulumi.Input['SqlDatabaseDataRetentionArgs']]):
        pulumi.set(self, "data_retention", value)

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
    @pulumi.getter(name="sqlDatabaseName")
    def sql_database_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the sql database.
        """
        return pulumi.get(self, "sql_database_name")

    @sql_database_name.setter
    def sql_database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sql_database_name", value)

    @property
    @pulumi.getter(name="storageRedundancy")
    def storage_redundancy(self) -> Optional[pulumi.Input[Union[str, 'StorageRedundancy']]]:
        """
        The storage redundancy of the database.
        """
        return pulumi.get(self, "storage_redundancy")

    @storage_redundancy.setter
    def storage_redundancy(self, value: Optional[pulumi.Input[Union[str, 'StorageRedundancy']]]):
        pulumi.set(self, "storage_redundancy", value)

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


class SqlDatabase(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 data_retention: Optional[pulumi.Input[pulumi.InputType['SqlDatabaseDataRetentionArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_database_name: Optional[pulumi.Input[str]] = None,
                 storage_redundancy: Optional[pulumi.Input[Union[str, 'StorageRedundancy']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A sql database resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] collation: The collation of the database.
        :param pulumi.Input[pulumi.InputType['SqlDatabaseDataRetentionArgs']] data_retention: Sql database data retention.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] sql_database_name: The name of the sql database.
        :param pulumi.Input[Union[str, 'StorageRedundancy']] storage_redundancy: The storage redundancy of the database.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SqlDatabaseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A sql database resource.

        :param str resource_name: The name of the resource.
        :param SqlDatabaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SqlDatabaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 data_retention: Optional[pulumi.Input[pulumi.InputType['SqlDatabaseDataRetentionArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_database_name: Optional[pulumi.Input[str]] = None,
                 storage_redundancy: Optional[pulumi.Input[Union[str, 'StorageRedundancy']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = SqlDatabaseArgs.__new__(SqlDatabaseArgs)

            __props__.__dict__["collation"] = collation
            __props__.__dict__["data_retention"] = data_retention
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sql_database_name"] = sql_database_name
            __props__.__dict__["storage_redundancy"] = storage_redundancy
            __props__.__dict__["tags"] = tags
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["database_guid"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        super(SqlDatabase, __self__).__init__(
            'azure-native:synapse/v20200401preview:SqlDatabase',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SqlDatabase':
        """
        Get an existing SqlDatabase resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SqlDatabaseArgs.__new__(SqlDatabaseArgs)

        __props__.__dict__["collation"] = None
        __props__.__dict__["data_retention"] = None
        __props__.__dict__["database_guid"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["storage_redundancy"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return SqlDatabase(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def collation(self) -> pulumi.Output[Optional[str]]:
        """
        The collation of the database.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="dataRetention")
    def data_retention(self) -> pulumi.Output[Optional['outputs.SqlDatabaseDataRetentionResponse']]:
        """
        Sql database data retention.
        """
        return pulumi.get(self, "data_retention")

    @property
    @pulumi.getter(name="databaseGuid")
    def database_guid(self) -> pulumi.Output[str]:
        """
        The Guid of the database.
        """
        return pulumi.get(self, "database_guid")

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
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the database.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageRedundancy")
    def storage_redundancy(self) -> pulumi.Output[Optional[str]]:
        """
        The storage redundancy of the database.
        """
        return pulumi.get(self, "storage_redundancy")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        SystemData of SqlDatabase.
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

