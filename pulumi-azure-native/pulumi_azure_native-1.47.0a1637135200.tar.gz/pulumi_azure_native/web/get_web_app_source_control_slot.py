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
    'GetWebAppSourceControlSlotResult',
    'AwaitableGetWebAppSourceControlSlotResult',
    'get_web_app_source_control_slot',
    'get_web_app_source_control_slot_output',
]

@pulumi.output_type
class GetWebAppSourceControlSlotResult:
    """
    Source control configuration for an app.
    """
    def __init__(__self__, branch=None, deployment_rollback_enabled=None, git_hub_action_configuration=None, id=None, is_git_hub_action=None, is_manual_integration=None, is_mercurial=None, kind=None, name=None, repo_url=None, type=None):
        if branch and not isinstance(branch, str):
            raise TypeError("Expected argument 'branch' to be a str")
        pulumi.set(__self__, "branch", branch)
        if deployment_rollback_enabled and not isinstance(deployment_rollback_enabled, bool):
            raise TypeError("Expected argument 'deployment_rollback_enabled' to be a bool")
        pulumi.set(__self__, "deployment_rollback_enabled", deployment_rollback_enabled)
        if git_hub_action_configuration and not isinstance(git_hub_action_configuration, dict):
            raise TypeError("Expected argument 'git_hub_action_configuration' to be a dict")
        pulumi.set(__self__, "git_hub_action_configuration", git_hub_action_configuration)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_git_hub_action and not isinstance(is_git_hub_action, bool):
            raise TypeError("Expected argument 'is_git_hub_action' to be a bool")
        pulumi.set(__self__, "is_git_hub_action", is_git_hub_action)
        if is_manual_integration and not isinstance(is_manual_integration, bool):
            raise TypeError("Expected argument 'is_manual_integration' to be a bool")
        pulumi.set(__self__, "is_manual_integration", is_manual_integration)
        if is_mercurial and not isinstance(is_mercurial, bool):
            raise TypeError("Expected argument 'is_mercurial' to be a bool")
        pulumi.set(__self__, "is_mercurial", is_mercurial)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if repo_url and not isinstance(repo_url, str):
            raise TypeError("Expected argument 'repo_url' to be a str")
        pulumi.set(__self__, "repo_url", repo_url)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def branch(self) -> Optional[str]:
        """
        Name of branch to use for deployment.
        """
        return pulumi.get(self, "branch")

    @property
    @pulumi.getter(name="deploymentRollbackEnabled")
    def deployment_rollback_enabled(self) -> Optional[bool]:
        """
        <code>true</code> to enable deployment rollback; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "deployment_rollback_enabled")

    @property
    @pulumi.getter(name="gitHubActionConfiguration")
    def git_hub_action_configuration(self) -> Optional['outputs.GitHubActionConfigurationResponse']:
        """
        If GitHub Action is selected, than the associated configuration.
        """
        return pulumi.get(self, "git_hub_action_configuration")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isGitHubAction")
    def is_git_hub_action(self) -> Optional[bool]:
        """
        <code>true</code> if this is deployed via GitHub action.
        """
        return pulumi.get(self, "is_git_hub_action")

    @property
    @pulumi.getter(name="isManualIntegration")
    def is_manual_integration(self) -> Optional[bool]:
        """
        <code>true</code> to limit to manual integration; <code>false</code> to enable continuous integration (which configures webhooks into online repos like GitHub).
        """
        return pulumi.get(self, "is_manual_integration")

    @property
    @pulumi.getter(name="isMercurial")
    def is_mercurial(self) -> Optional[bool]:
        """
        <code>true</code> for a Mercurial repository; <code>false</code> for a Git repository.
        """
        return pulumi.get(self, "is_mercurial")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="repoUrl")
    def repo_url(self) -> Optional[str]:
        """
        Repository or source control URL.
        """
        return pulumi.get(self, "repo_url")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWebAppSourceControlSlotResult(GetWebAppSourceControlSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebAppSourceControlSlotResult(
            branch=self.branch,
            deployment_rollback_enabled=self.deployment_rollback_enabled,
            git_hub_action_configuration=self.git_hub_action_configuration,
            id=self.id,
            is_git_hub_action=self.is_git_hub_action,
            is_manual_integration=self.is_manual_integration,
            is_mercurial=self.is_mercurial,
            kind=self.kind,
            name=self.name,
            repo_url=self.repo_url,
            type=self.type)


def get_web_app_source_control_slot(name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    slot: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebAppSourceControlSlotResult:
    """
    Source control configuration for an app.
    API Version: 2020-12-01.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get the source control configuration for the production slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:web:getWebAppSourceControlSlot', __args__, opts=opts, typ=GetWebAppSourceControlSlotResult).value

    return AwaitableGetWebAppSourceControlSlotResult(
        branch=__ret__.branch,
        deployment_rollback_enabled=__ret__.deployment_rollback_enabled,
        git_hub_action_configuration=__ret__.git_hub_action_configuration,
        id=__ret__.id,
        is_git_hub_action=__ret__.is_git_hub_action,
        is_manual_integration=__ret__.is_manual_integration,
        is_mercurial=__ret__.is_mercurial,
        kind=__ret__.kind,
        name=__ret__.name,
        repo_url=__ret__.repo_url,
        type=__ret__.type)


@_utilities.lift_output_func(get_web_app_source_control_slot)
def get_web_app_source_control_slot_output(name: Optional[pulumi.Input[str]] = None,
                                           resource_group_name: Optional[pulumi.Input[str]] = None,
                                           slot: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebAppSourceControlSlotResult]:
    """
    Source control configuration for an app.
    API Version: 2020-12-01.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get the source control configuration for the production slot.
    """
    ...
