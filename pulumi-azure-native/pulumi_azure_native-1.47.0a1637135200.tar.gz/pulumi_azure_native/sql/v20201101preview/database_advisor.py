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

__all__ = ['DatabaseAdvisorArgs', 'DatabaseAdvisor']

@pulumi.input_type
class DatabaseAdvisorArgs:
    def __init__(__self__, *,
                 auto_execute_status: pulumi.Input['AutoExecuteStatus'],
                 database_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 advisor_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DatabaseAdvisor resource.
        :param pulumi.Input['AutoExecuteStatus'] auto_execute_status: Gets the auto-execute status (whether to let the system execute the recommendations) of this advisor. Possible values are 'Enabled' and 'Disabled'
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] advisor_name: The name of the Database Advisor.
        """
        pulumi.set(__self__, "auto_execute_status", auto_execute_status)
        pulumi.set(__self__, "database_name", database_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server_name", server_name)
        if advisor_name is not None:
            pulumi.set(__self__, "advisor_name", advisor_name)

    @property
    @pulumi.getter(name="autoExecuteStatus")
    def auto_execute_status(self) -> pulumi.Input['AutoExecuteStatus']:
        """
        Gets the auto-execute status (whether to let the system execute the recommendations) of this advisor. Possible values are 'Enabled' and 'Disabled'
        """
        return pulumi.get(self, "auto_execute_status")

    @auto_execute_status.setter
    def auto_execute_status(self, value: pulumi.Input['AutoExecuteStatus']):
        pulumi.set(self, "auto_execute_status", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Input[str]:
        """
        The name of the database.
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
    @pulumi.getter(name="advisorName")
    def advisor_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Database Advisor.
        """
        return pulumi.get(self, "advisor_name")

    @advisor_name.setter
    def advisor_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "advisor_name", value)


class DatabaseAdvisor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 advisor_name: Optional[pulumi.Input[str]] = None,
                 auto_execute_status: Optional[pulumi.Input['AutoExecuteStatus']] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Database, Server or Elastic Pool Advisor.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] advisor_name: The name of the Database Advisor.
        :param pulumi.Input['AutoExecuteStatus'] auto_execute_status: Gets the auto-execute status (whether to let the system execute the recommendations) of this advisor. Possible values are 'Enabled' and 'Disabled'
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatabaseAdvisorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Database, Server or Elastic Pool Advisor.

        :param str resource_name: The name of the resource.
        :param DatabaseAdvisorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseAdvisorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 advisor_name: Optional[pulumi.Input[str]] = None,
                 auto_execute_status: Optional[pulumi.Input['AutoExecuteStatus']] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = DatabaseAdvisorArgs.__new__(DatabaseAdvisorArgs)

            __props__.__dict__["advisor_name"] = advisor_name
            if auto_execute_status is None and not opts.urn:
                raise TypeError("Missing required property 'auto_execute_status'")
            __props__.__dict__["auto_execute_status"] = auto_execute_status
            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__["database_name"] = database_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["advisor_status"] = None
            __props__.__dict__["auto_execute_status_inherited_from"] = None
            __props__.__dict__["kind"] = None
            __props__.__dict__["last_checked"] = None
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["recommendations_status"] = None
            __props__.__dict__["recommended_actions"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:DatabaseAdvisor"), pulumi.Alias(type_="azure-native:sql/v20140401:DatabaseAdvisor"), pulumi.Alias(type_="azure-native:sql/v20150501preview:DatabaseAdvisor"), pulumi.Alias(type_="azure-native:sql/v20200202preview:DatabaseAdvisor"), pulumi.Alias(type_="azure-native:sql/v20200801preview:DatabaseAdvisor"), pulumi.Alias(type_="azure-native:sql/v20210201preview:DatabaseAdvisor"), pulumi.Alias(type_="azure-native:sql/v20210501preview:DatabaseAdvisor")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DatabaseAdvisor, __self__).__init__(
            'azure-native:sql/v20201101preview:DatabaseAdvisor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DatabaseAdvisor':
        """
        Get an existing DatabaseAdvisor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DatabaseAdvisorArgs.__new__(DatabaseAdvisorArgs)

        __props__.__dict__["advisor_status"] = None
        __props__.__dict__["auto_execute_status"] = None
        __props__.__dict__["auto_execute_status_inherited_from"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["last_checked"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["recommendations_status"] = None
        __props__.__dict__["recommended_actions"] = None
        __props__.__dict__["type"] = None
        return DatabaseAdvisor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="advisorStatus")
    def advisor_status(self) -> pulumi.Output[str]:
        """
        Gets the status of availability of this advisor to customers. Possible values are 'GA', 'PublicPreview', 'LimitedPublicPreview' and 'PrivatePreview'.
        """
        return pulumi.get(self, "advisor_status")

    @property
    @pulumi.getter(name="autoExecuteStatus")
    def auto_execute_status(self) -> pulumi.Output[str]:
        """
        Gets the auto-execute status (whether to let the system execute the recommendations) of this advisor. Possible values are 'Enabled' and 'Disabled'
        """
        return pulumi.get(self, "auto_execute_status")

    @property
    @pulumi.getter(name="autoExecuteStatusInheritedFrom")
    def auto_execute_status_inherited_from(self) -> pulumi.Output[str]:
        """
        Gets the resource from which current value of auto-execute status is inherited. Auto-execute status can be set on (and inherited from) different levels in the resource hierarchy. Possible values are 'Subscription', 'Server', 'ElasticPool', 'Database' and 'Default' (when status is not explicitly set on any level).
        """
        return pulumi.get(self, "auto_execute_status_inherited_from")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Resource kind.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastChecked")
    def last_checked(self) -> pulumi.Output[str]:
        """
        Gets the time when the current resource was analyzed for recommendations by this advisor.
        """
        return pulumi.get(self, "last_checked")

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
    @pulumi.getter(name="recommendationsStatus")
    def recommendations_status(self) -> pulumi.Output[str]:
        """
        Gets that status of recommendations for this advisor and reason for not having any recommendations. Possible values include, but are not limited to, 'Ok' (Recommendations available),LowActivity (not enough workload to analyze), 'DbSeemsTuned' (Database is doing well), etc.
        """
        return pulumi.get(self, "recommendations_status")

    @property
    @pulumi.getter(name="recommendedActions")
    def recommended_actions(self) -> pulumi.Output[Sequence['outputs.RecommendedActionResponse']]:
        """
        Gets the recommended actions for this advisor.
        """
        return pulumi.get(self, "recommended_actions")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

