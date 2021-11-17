# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['SavedSearchArgs', 'SavedSearch']

@pulumi.input_type
class SavedSearchArgs:
    def __init__(__self__, *,
                 category: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 query: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 etag: Optional[pulumi.Input[str]] = None,
                 function_alias: Optional[pulumi.Input[str]] = None,
                 function_parameters: Optional[pulumi.Input[str]] = None,
                 saved_search_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['TagArgs']]]] = None,
                 version: Optional[pulumi.Input[float]] = None):
        """
        The set of arguments for constructing a SavedSearch resource.
        :param pulumi.Input[str] category: The category of the saved search. This helps the user to find a saved search faster. 
        :param pulumi.Input[str] display_name: Saved search display name.
        :param pulumi.Input[str] query: The query expression for the saved search.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] etag: The ETag of the saved search. To override an existing saved search, use "*" or specify the current Etag
        :param pulumi.Input[str] function_alias: The function alias if query serves as a function.
        :param pulumi.Input[str] function_parameters: The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://docs.microsoft.com/en-us/azure/kusto/query/functions/user-defined-functions.
        :param pulumi.Input[str] saved_search_id: The id of the saved search.
        :param pulumi.Input[Sequence[pulumi.Input['TagArgs']]] tags: The tags attached to the saved search.
        :param pulumi.Input[float] version: The version number of the query language. The current version is 2 and is the default.
        """
        pulumi.set(__self__, "category", category)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "query", query)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if function_alias is not None:
            pulumi.set(__self__, "function_alias", function_alias)
        if function_parameters is not None:
            pulumi.set(__self__, "function_parameters", function_parameters)
        if saved_search_id is not None:
            pulumi.set(__self__, "saved_search_id", saved_search_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Input[str]:
        """
        The category of the saved search. This helps the user to find a saved search faster. 
        """
        return pulumi.get(self, "category")

    @category.setter
    def category(self, value: pulumi.Input[str]):
        pulumi.set(self, "category", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Saved search display name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def query(self) -> pulumi.Input[str]:
        """
        The query expression for the saved search.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: pulumi.Input[str]):
        pulumi.set(self, "query", value)

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
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        The ETag of the saved search. To override an existing saved search, use "*" or specify the current Etag
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter(name="functionAlias")
    def function_alias(self) -> Optional[pulumi.Input[str]]:
        """
        The function alias if query serves as a function.
        """
        return pulumi.get(self, "function_alias")

    @function_alias.setter
    def function_alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function_alias", value)

    @property
    @pulumi.getter(name="functionParameters")
    def function_parameters(self) -> Optional[pulumi.Input[str]]:
        """
        The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://docs.microsoft.com/en-us/azure/kusto/query/functions/user-defined-functions.
        """
        return pulumi.get(self, "function_parameters")

    @function_parameters.setter
    def function_parameters(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function_parameters", value)

    @property
    @pulumi.getter(name="savedSearchId")
    def saved_search_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the saved search.
        """
        return pulumi.get(self, "saved_search_id")

    @saved_search_id.setter
    def saved_search_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "saved_search_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TagArgs']]]]:
        """
        The tags attached to the saved search.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[float]]:
        """
        The version number of the query language. The current version is 2 and is the default.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "version", value)


class SavedSearch(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 function_alias: Optional[pulumi.Input[str]] = None,
                 function_parameters: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 saved_search_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TagArgs']]]]] = None,
                 version: Optional[pulumi.Input[float]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Value object for saved search results.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] category: The category of the saved search. This helps the user to find a saved search faster. 
        :param pulumi.Input[str] display_name: Saved search display name.
        :param pulumi.Input[str] etag: The ETag of the saved search. To override an existing saved search, use "*" or specify the current Etag
        :param pulumi.Input[str] function_alias: The function alias if query serves as a function.
        :param pulumi.Input[str] function_parameters: The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://docs.microsoft.com/en-us/azure/kusto/query/functions/user-defined-functions.
        :param pulumi.Input[str] query: The query expression for the saved search.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] saved_search_id: The id of the saved search.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TagArgs']]]] tags: The tags attached to the saved search.
        :param pulumi.Input[float] version: The version number of the query language. The current version is 2 and is the default.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SavedSearchArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Value object for saved search results.

        :param str resource_name: The name of the resource.
        :param SavedSearchArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SavedSearchArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 function_alias: Optional[pulumi.Input[str]] = None,
                 function_parameters: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 saved_search_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TagArgs']]]]] = None,
                 version: Optional[pulumi.Input[float]] = None,
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
            __props__ = SavedSearchArgs.__new__(SavedSearchArgs)

            if category is None and not opts.urn:
                raise TypeError("Missing required property 'category'")
            __props__.__dict__["category"] = category
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["etag"] = etag
            __props__.__dict__["function_alias"] = function_alias
            __props__.__dict__["function_parameters"] = function_parameters
            if query is None and not opts.urn:
                raise TypeError("Missing required property 'query'")
            __props__.__dict__["query"] = query
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["saved_search_id"] = saved_search_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["version"] = version
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:operationalinsights:SavedSearch"), pulumi.Alias(type_="azure-native:operationalinsights/v20150320:SavedSearch"), pulumi.Alias(type_="azure-native:operationalinsights/v20200301preview:SavedSearch")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SavedSearch, __self__).__init__(
            'azure-native:operationalinsights/v20200801:SavedSearch',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SavedSearch':
        """
        Get an existing SavedSearch resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SavedSearchArgs.__new__(SavedSearchArgs)

        __props__.__dict__["category"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["function_alias"] = None
        __props__.__dict__["function_parameters"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["query"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["version"] = None
        return SavedSearch(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Output[str]:
        """
        The category of the saved search. This helps the user to find a saved search faster. 
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Saved search display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        The ETag of the saved search. To override an existing saved search, use "*" or specify the current Etag
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="functionAlias")
    def function_alias(self) -> pulumi.Output[Optional[str]]:
        """
        The function alias if query serves as a function.
        """
        return pulumi.get(self, "function_alias")

    @property
    @pulumi.getter(name="functionParameters")
    def function_parameters(self) -> pulumi.Output[Optional[str]]:
        """
        The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://docs.microsoft.com/en-us/azure/kusto/query/functions/user-defined-functions.
        """
        return pulumi.get(self, "function_parameters")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> pulumi.Output[str]:
        """
        The query expression for the saved search.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.TagResponse']]]:
        """
        The tags attached to the saved search.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[float]]:
        """
        The version number of the query language. The current version is 2 and is the default.
        """
        return pulumi.get(self, "version")

