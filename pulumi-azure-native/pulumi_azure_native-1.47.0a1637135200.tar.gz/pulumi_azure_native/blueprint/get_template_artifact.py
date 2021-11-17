# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetTemplateArtifactResult',
    'AwaitableGetTemplateArtifactResult',
    'get_template_artifact',
    'get_template_artifact_output',
]

@pulumi.output_type
class GetTemplateArtifactResult:
    """
    Blueprint artifact that deploys a Resource Manager template.
    """
    def __init__(__self__, depends_on=None, description=None, display_name=None, id=None, kind=None, name=None, parameters=None, resource_group=None, template=None, type=None):
        if depends_on and not isinstance(depends_on, list):
            raise TypeError("Expected argument 'depends_on' to be a list")
        pulumi.set(__self__, "depends_on", depends_on)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if resource_group and not isinstance(resource_group, str):
            raise TypeError("Expected argument 'resource_group' to be a str")
        pulumi.set(__self__, "resource_group", resource_group)
        if template and not isinstance(template, dict):
            raise TypeError("Expected argument 'template' to be a dict")
        pulumi.set(__self__, "template", template)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dependsOn")
    def depends_on(self) -> Optional[Sequence[str]]:
        """
        Artifacts which need to be deployed before the specified artifact.
        """
        return pulumi.get(self, "depends_on")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Multi-line explain this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        One-liner string explain this resource.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        String Id used to locate any resource on Azure.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Specifies the kind of blueprint artifact.
        Expected value is 'template'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of this resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Mapping[str, 'outputs.ParameterValueResponse']:
        """
        Resource Manager template blueprint artifact parameter values.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> Optional[str]:
        """
        If applicable, the name of the resource group placeholder to which the Resource Manager template blueprint artifact will be deployed.
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter
    def template(self) -> Any:
        """
        The Resource Manager template blueprint artifact body.
        """
        return pulumi.get(self, "template")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of this resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetTemplateArtifactResult(GetTemplateArtifactResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTemplateArtifactResult(
            depends_on=self.depends_on,
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            kind=self.kind,
            name=self.name,
            parameters=self.parameters,
            resource_group=self.resource_group,
            template=self.template,
            type=self.type)


def get_template_artifact(artifact_name: Optional[str] = None,
                          blueprint_name: Optional[str] = None,
                          resource_scope: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTemplateArtifactResult:
    """
    Blueprint artifact that deploys a Resource Manager template.
    API Version: 2018-11-01-preview.


    :param str artifact_name: Name of the blueprint artifact.
    :param str blueprint_name: Name of the blueprint definition.
    :param str resource_scope: The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
    """
    __args__ = dict()
    __args__['artifactName'] = artifact_name
    __args__['blueprintName'] = blueprint_name
    __args__['resourceScope'] = resource_scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:blueprint:getTemplateArtifact', __args__, opts=opts, typ=GetTemplateArtifactResult).value

    return AwaitableGetTemplateArtifactResult(
        depends_on=__ret__.depends_on,
        description=__ret__.description,
        display_name=__ret__.display_name,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        parameters=__ret__.parameters,
        resource_group=__ret__.resource_group,
        template=__ret__.template,
        type=__ret__.type)


@_utilities.lift_output_func(get_template_artifact)
def get_template_artifact_output(artifact_name: Optional[pulumi.Input[str]] = None,
                                 blueprint_name: Optional[pulumi.Input[str]] = None,
                                 resource_scope: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTemplateArtifactResult]:
    """
    Blueprint artifact that deploys a Resource Manager template.
    API Version: 2018-11-01-preview.


    :param str artifact_name: Name of the blueprint artifact.
    :param str blueprint_name: Name of the blueprint definition.
    :param str resource_scope: The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
    """
    ...
