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

__all__ = ['PolicySetDefinitionAtManagementGroupArgs', 'PolicySetDefinitionAtManagementGroup']

@pulumi.input_type
class PolicySetDefinitionAtManagementGroupArgs:
    def __init__(__self__, *,
                 management_group_id: pulumi.Input[str],
                 policy_definitions: pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionReferenceArgs']]],
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[Any] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionsValueArgs']]]] = None,
                 policy_definition_groups: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionGroupArgs']]]] = None,
                 policy_set_definition_name: Optional[pulumi.Input[str]] = None,
                 policy_type: Optional[pulumi.Input[Union[str, 'PolicyType']]] = None):
        """
        The set of arguments for constructing a PolicySetDefinitionAtManagementGroup resource.
        :param pulumi.Input[str] management_group_id: The ID of the management group.
        :param pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionReferenceArgs']]] policy_definitions: An array of policy definition references.
        :param pulumi.Input[str] description: The policy set definition description.
        :param pulumi.Input[str] display_name: The display name of the policy set definition.
        :param Any metadata: The policy set definition metadata.  Metadata is an open ended object and is typically a collection of key value pairs.
        :param pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionsValueArgs']]] parameters: The policy set definition parameters that can be used in policy definition references.
        :param pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionGroupArgs']]] policy_definition_groups: The metadata describing groups of policy definition references within the policy set definition.
        :param pulumi.Input[str] policy_set_definition_name: The name of the policy set definition to create.
        :param pulumi.Input[Union[str, 'PolicyType']] policy_type: The type of policy definition. Possible values are NotSpecified, BuiltIn, Custom, and Static.
        """
        pulumi.set(__self__, "management_group_id", management_group_id)
        pulumi.set(__self__, "policy_definitions", policy_definitions)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if metadata is not None:
            pulumi.set(__self__, "metadata", metadata)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if policy_definition_groups is not None:
            pulumi.set(__self__, "policy_definition_groups", policy_definition_groups)
        if policy_set_definition_name is not None:
            pulumi.set(__self__, "policy_set_definition_name", policy_set_definition_name)
        if policy_type is not None:
            pulumi.set(__self__, "policy_type", policy_type)

    @property
    @pulumi.getter(name="managementGroupId")
    def management_group_id(self) -> pulumi.Input[str]:
        """
        The ID of the management group.
        """
        return pulumi.get(self, "management_group_id")

    @management_group_id.setter
    def management_group_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "management_group_id", value)

    @property
    @pulumi.getter(name="policyDefinitions")
    def policy_definitions(self) -> pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionReferenceArgs']]]:
        """
        An array of policy definition references.
        """
        return pulumi.get(self, "policy_definitions")

    @policy_definitions.setter
    def policy_definitions(self, value: pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionReferenceArgs']]]):
        pulumi.set(self, "policy_definitions", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The policy set definition description.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The display name of the policy set definition.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def metadata(self) -> Optional[Any]:
        """
        The policy set definition metadata.  Metadata is an open ended object and is typically a collection of key value pairs.
        """
        return pulumi.get(self, "metadata")

    @metadata.setter
    def metadata(self, value: Optional[Any]):
        pulumi.set(self, "metadata", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionsValueArgs']]]]:
        """
        The policy set definition parameters that can be used in policy definition references.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['ParameterDefinitionsValueArgs']]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="policyDefinitionGroups")
    def policy_definition_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionGroupArgs']]]]:
        """
        The metadata describing groups of policy definition references within the policy set definition.
        """
        return pulumi.get(self, "policy_definition_groups")

    @policy_definition_groups.setter
    def policy_definition_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PolicyDefinitionGroupArgs']]]]):
        pulumi.set(self, "policy_definition_groups", value)

    @property
    @pulumi.getter(name="policySetDefinitionName")
    def policy_set_definition_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the policy set definition to create.
        """
        return pulumi.get(self, "policy_set_definition_name")

    @policy_set_definition_name.setter
    def policy_set_definition_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy_set_definition_name", value)

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> Optional[pulumi.Input[Union[str, 'PolicyType']]]:
        """
        The type of policy definition. Possible values are NotSpecified, BuiltIn, Custom, and Static.
        """
        return pulumi.get(self, "policy_type")

    @policy_type.setter
    def policy_type(self, value: Optional[pulumi.Input[Union[str, 'PolicyType']]]):
        pulumi.set(self, "policy_type", value)


class PolicySetDefinitionAtManagementGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 management_group_id: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[Any] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterDefinitionsValueArgs']]]]] = None,
                 policy_definition_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyDefinitionGroupArgs']]]]] = None,
                 policy_definitions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyDefinitionReferenceArgs']]]]] = None,
                 policy_set_definition_name: Optional[pulumi.Input[str]] = None,
                 policy_type: Optional[pulumi.Input[Union[str, 'PolicyType']]] = None,
                 __props__=None):
        """
        The policy set definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The policy set definition description.
        :param pulumi.Input[str] display_name: The display name of the policy set definition.
        :param pulumi.Input[str] management_group_id: The ID of the management group.
        :param Any metadata: The policy set definition metadata.  Metadata is an open ended object and is typically a collection of key value pairs.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterDefinitionsValueArgs']]]] parameters: The policy set definition parameters that can be used in policy definition references.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyDefinitionGroupArgs']]]] policy_definition_groups: The metadata describing groups of policy definition references within the policy set definition.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyDefinitionReferenceArgs']]]] policy_definitions: An array of policy definition references.
        :param pulumi.Input[str] policy_set_definition_name: The name of the policy set definition to create.
        :param pulumi.Input[Union[str, 'PolicyType']] policy_type: The type of policy definition. Possible values are NotSpecified, BuiltIn, Custom, and Static.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PolicySetDefinitionAtManagementGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The policy set definition.

        :param str resource_name: The name of the resource.
        :param PolicySetDefinitionAtManagementGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PolicySetDefinitionAtManagementGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 management_group_id: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[Any] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterDefinitionsValueArgs']]]]] = None,
                 policy_definition_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyDefinitionGroupArgs']]]]] = None,
                 policy_definitions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyDefinitionReferenceArgs']]]]] = None,
                 policy_set_definition_name: Optional[pulumi.Input[str]] = None,
                 policy_type: Optional[pulumi.Input[Union[str, 'PolicyType']]] = None,
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
            __props__ = PolicySetDefinitionAtManagementGroupArgs.__new__(PolicySetDefinitionAtManagementGroupArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["display_name"] = display_name
            if management_group_id is None and not opts.urn:
                raise TypeError("Missing required property 'management_group_id'")
            __props__.__dict__["management_group_id"] = management_group_id
            __props__.__dict__["metadata"] = metadata
            __props__.__dict__["parameters"] = parameters
            __props__.__dict__["policy_definition_groups"] = policy_definition_groups
            if policy_definitions is None and not opts.urn:
                raise TypeError("Missing required property 'policy_definitions'")
            __props__.__dict__["policy_definitions"] = policy_definitions
            __props__.__dict__["policy_set_definition_name"] = policy_set_definition_name
            __props__.__dict__["policy_type"] = policy_type
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:authorization:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20170601preview:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20180301:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20180501:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20190101:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20190601:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20200301:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20200901:PolicySetDefinitionAtManagementGroup"), pulumi.Alias(type_="azure-native:authorization/v20210601:PolicySetDefinitionAtManagementGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PolicySetDefinitionAtManagementGroup, __self__).__init__(
            'azure-native:authorization/v20190901:PolicySetDefinitionAtManagementGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PolicySetDefinitionAtManagementGroup':
        """
        Get an existing PolicySetDefinitionAtManagementGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PolicySetDefinitionAtManagementGroupArgs.__new__(PolicySetDefinitionAtManagementGroupArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["metadata"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["parameters"] = None
        __props__.__dict__["policy_definition_groups"] = None
        __props__.__dict__["policy_definitions"] = None
        __props__.__dict__["policy_type"] = None
        __props__.__dict__["type"] = None
        return PolicySetDefinitionAtManagementGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The policy set definition description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        The display name of the policy set definition.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional[Any]]:
        """
        The policy set definition metadata.  Metadata is an open ended object and is typically a collection of key value pairs.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the policy set definition.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Optional[Mapping[str, 'outputs.ParameterDefinitionsValueResponse']]]:
        """
        The policy set definition parameters that can be used in policy definition references.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionGroups")
    def policy_definition_groups(self) -> pulumi.Output[Optional[Sequence['outputs.PolicyDefinitionGroupResponse']]]:
        """
        The metadata describing groups of policy definition references within the policy set definition.
        """
        return pulumi.get(self, "policy_definition_groups")

    @property
    @pulumi.getter(name="policyDefinitions")
    def policy_definitions(self) -> pulumi.Output[Sequence['outputs.PolicyDefinitionReferenceResponse']]:
        """
        An array of policy definition references.
        """
        return pulumi.get(self, "policy_definitions")

    @property
    @pulumi.getter(name="policyType")
    def policy_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of policy definition. Possible values are NotSpecified, BuiltIn, Custom, and Static.
        """
        return pulumi.get(self, "policy_type")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource (Microsoft.Authorization/policySetDefinitions).
        """
        return pulumi.get(self, "type")

