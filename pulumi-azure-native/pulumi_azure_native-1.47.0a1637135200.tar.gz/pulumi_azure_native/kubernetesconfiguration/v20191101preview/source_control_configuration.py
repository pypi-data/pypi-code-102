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

__all__ = ['SourceControlConfigurationArgs', 'SourceControlConfiguration']

@pulumi.input_type
class SourceControlConfigurationArgs:
    def __init__(__self__, *,
                 cluster_name: pulumi.Input[str],
                 cluster_resource_name: pulumi.Input[str],
                 cluster_rp: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 enable_helm_operator: Optional[pulumi.Input[Union[str, 'EnableHelmOperator']]] = None,
                 helm_operator_properties: Optional[pulumi.Input['HelmOperatorPropertiesArgs']] = None,
                 operator_instance_name: Optional[pulumi.Input[str]] = None,
                 operator_namespace: Optional[pulumi.Input[str]] = None,
                 operator_params: Optional[pulumi.Input[str]] = None,
                 operator_scope: Optional[pulumi.Input[Union[str, 'OperatorScope']]] = None,
                 operator_type: Optional[pulumi.Input[Union[str, 'OperatorType']]] = None,
                 repository_url: Optional[pulumi.Input[str]] = None,
                 source_control_configuration_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SourceControlConfiguration resource.
        :param pulumi.Input[str] cluster_name: The name of the kubernetes cluster.
        :param pulumi.Input[str] cluster_resource_name: The Kubernetes cluster resource name - either managedClusters (for AKS clusters) or connectedClusters (for OnPrem K8S clusters).
        :param pulumi.Input[str] cluster_rp: The Kubernetes cluster RP - either Microsoft.ContainerService (for AKS clusters) or Microsoft.Kubernetes (for OnPrem K8S clusters).
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'EnableHelmOperator']] enable_helm_operator: Option to enable Helm Operator for this git configuration.
        :param pulumi.Input['HelmOperatorPropertiesArgs'] helm_operator_properties: Properties for Helm operator.
        :param pulumi.Input[str] operator_instance_name: Instance name of the operator - identifying the specific configuration.
        :param pulumi.Input[str] operator_namespace: The namespace to which this operator is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        :param pulumi.Input[str] operator_params: Any Parameters for the Operator instance in string format.
        :param pulumi.Input[Union[str, 'OperatorScope']] operator_scope: Scope at which the operator will be installed.
        :param pulumi.Input[Union[str, 'OperatorType']] operator_type: Type of the operator
        :param pulumi.Input[str] repository_url: Url of the SourceControl Repository.
        :param pulumi.Input[str] source_control_configuration_name: Name of the Source Control Configuration.
        """
        pulumi.set(__self__, "cluster_name", cluster_name)
        pulumi.set(__self__, "cluster_resource_name", cluster_resource_name)
        pulumi.set(__self__, "cluster_rp", cluster_rp)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if enable_helm_operator is not None:
            pulumi.set(__self__, "enable_helm_operator", enable_helm_operator)
        if helm_operator_properties is not None:
            pulumi.set(__self__, "helm_operator_properties", helm_operator_properties)
        if operator_instance_name is not None:
            pulumi.set(__self__, "operator_instance_name", operator_instance_name)
        if operator_namespace is None:
            operator_namespace = 'default'
        if operator_namespace is not None:
            pulumi.set(__self__, "operator_namespace", operator_namespace)
        if operator_params is not None:
            pulumi.set(__self__, "operator_params", operator_params)
        if operator_scope is None:
            operator_scope = 'cluster'
        if operator_scope is not None:
            pulumi.set(__self__, "operator_scope", operator_scope)
        if operator_type is not None:
            pulumi.set(__self__, "operator_type", operator_type)
        if repository_url is not None:
            pulumi.set(__self__, "repository_url", repository_url)
        if source_control_configuration_name is not None:
            pulumi.set(__self__, "source_control_configuration_name", source_control_configuration_name)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Input[str]:
        """
        The name of the kubernetes cluster.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="clusterResourceName")
    def cluster_resource_name(self) -> pulumi.Input[str]:
        """
        The Kubernetes cluster resource name - either managedClusters (for AKS clusters) or connectedClusters (for OnPrem K8S clusters).
        """
        return pulumi.get(self, "cluster_resource_name")

    @cluster_resource_name.setter
    def cluster_resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_resource_name", value)

    @property
    @pulumi.getter(name="clusterRp")
    def cluster_rp(self) -> pulumi.Input[str]:
        """
        The Kubernetes cluster RP - either Microsoft.ContainerService (for AKS clusters) or Microsoft.Kubernetes (for OnPrem K8S clusters).
        """
        return pulumi.get(self, "cluster_rp")

    @cluster_rp.setter
    def cluster_rp(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_rp", value)

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
    @pulumi.getter(name="enableHelmOperator")
    def enable_helm_operator(self) -> Optional[pulumi.Input[Union[str, 'EnableHelmOperator']]]:
        """
        Option to enable Helm Operator for this git configuration.
        """
        return pulumi.get(self, "enable_helm_operator")

    @enable_helm_operator.setter
    def enable_helm_operator(self, value: Optional[pulumi.Input[Union[str, 'EnableHelmOperator']]]):
        pulumi.set(self, "enable_helm_operator", value)

    @property
    @pulumi.getter(name="helmOperatorProperties")
    def helm_operator_properties(self) -> Optional[pulumi.Input['HelmOperatorPropertiesArgs']]:
        """
        Properties for Helm operator.
        """
        return pulumi.get(self, "helm_operator_properties")

    @helm_operator_properties.setter
    def helm_operator_properties(self, value: Optional[pulumi.Input['HelmOperatorPropertiesArgs']]):
        pulumi.set(self, "helm_operator_properties", value)

    @property
    @pulumi.getter(name="operatorInstanceName")
    def operator_instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        Instance name of the operator - identifying the specific configuration.
        """
        return pulumi.get(self, "operator_instance_name")

    @operator_instance_name.setter
    def operator_instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "operator_instance_name", value)

    @property
    @pulumi.getter(name="operatorNamespace")
    def operator_namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to which this operator is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        """
        return pulumi.get(self, "operator_namespace")

    @operator_namespace.setter
    def operator_namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "operator_namespace", value)

    @property
    @pulumi.getter(name="operatorParams")
    def operator_params(self) -> Optional[pulumi.Input[str]]:
        """
        Any Parameters for the Operator instance in string format.
        """
        return pulumi.get(self, "operator_params")

    @operator_params.setter
    def operator_params(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "operator_params", value)

    @property
    @pulumi.getter(name="operatorScope")
    def operator_scope(self) -> Optional[pulumi.Input[Union[str, 'OperatorScope']]]:
        """
        Scope at which the operator will be installed.
        """
        return pulumi.get(self, "operator_scope")

    @operator_scope.setter
    def operator_scope(self, value: Optional[pulumi.Input[Union[str, 'OperatorScope']]]):
        pulumi.set(self, "operator_scope", value)

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> Optional[pulumi.Input[Union[str, 'OperatorType']]]:
        """
        Type of the operator
        """
        return pulumi.get(self, "operator_type")

    @operator_type.setter
    def operator_type(self, value: Optional[pulumi.Input[Union[str, 'OperatorType']]]):
        pulumi.set(self, "operator_type", value)

    @property
    @pulumi.getter(name="repositoryUrl")
    def repository_url(self) -> Optional[pulumi.Input[str]]:
        """
        Url of the SourceControl Repository.
        """
        return pulumi.get(self, "repository_url")

    @repository_url.setter
    def repository_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repository_url", value)

    @property
    @pulumi.getter(name="sourceControlConfigurationName")
    def source_control_configuration_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Source Control Configuration.
        """
        return pulumi.get(self, "source_control_configuration_name")

    @source_control_configuration_name.setter
    def source_control_configuration_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_control_configuration_name", value)


class SourceControlConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 cluster_resource_name: Optional[pulumi.Input[str]] = None,
                 cluster_rp: Optional[pulumi.Input[str]] = None,
                 enable_helm_operator: Optional[pulumi.Input[Union[str, 'EnableHelmOperator']]] = None,
                 helm_operator_properties: Optional[pulumi.Input[pulumi.InputType['HelmOperatorPropertiesArgs']]] = None,
                 operator_instance_name: Optional[pulumi.Input[str]] = None,
                 operator_namespace: Optional[pulumi.Input[str]] = None,
                 operator_params: Optional[pulumi.Input[str]] = None,
                 operator_scope: Optional[pulumi.Input[Union[str, 'OperatorScope']]] = None,
                 operator_type: Optional[pulumi.Input[Union[str, 'OperatorType']]] = None,
                 repository_url: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 source_control_configuration_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The SourceControl Configuration object.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: The name of the kubernetes cluster.
        :param pulumi.Input[str] cluster_resource_name: The Kubernetes cluster resource name - either managedClusters (for AKS clusters) or connectedClusters (for OnPrem K8S clusters).
        :param pulumi.Input[str] cluster_rp: The Kubernetes cluster RP - either Microsoft.ContainerService (for AKS clusters) or Microsoft.Kubernetes (for OnPrem K8S clusters).
        :param pulumi.Input[Union[str, 'EnableHelmOperator']] enable_helm_operator: Option to enable Helm Operator for this git configuration.
        :param pulumi.Input[pulumi.InputType['HelmOperatorPropertiesArgs']] helm_operator_properties: Properties for Helm operator.
        :param pulumi.Input[str] operator_instance_name: Instance name of the operator - identifying the specific configuration.
        :param pulumi.Input[str] operator_namespace: The namespace to which this operator is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        :param pulumi.Input[str] operator_params: Any Parameters for the Operator instance in string format.
        :param pulumi.Input[Union[str, 'OperatorScope']] operator_scope: Scope at which the operator will be installed.
        :param pulumi.Input[Union[str, 'OperatorType']] operator_type: Type of the operator
        :param pulumi.Input[str] repository_url: Url of the SourceControl Repository.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] source_control_configuration_name: Name of the Source Control Configuration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SourceControlConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The SourceControl Configuration object.

        :param str resource_name: The name of the resource.
        :param SourceControlConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SourceControlConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 cluster_resource_name: Optional[pulumi.Input[str]] = None,
                 cluster_rp: Optional[pulumi.Input[str]] = None,
                 enable_helm_operator: Optional[pulumi.Input[Union[str, 'EnableHelmOperator']]] = None,
                 helm_operator_properties: Optional[pulumi.Input[pulumi.InputType['HelmOperatorPropertiesArgs']]] = None,
                 operator_instance_name: Optional[pulumi.Input[str]] = None,
                 operator_namespace: Optional[pulumi.Input[str]] = None,
                 operator_params: Optional[pulumi.Input[str]] = None,
                 operator_scope: Optional[pulumi.Input[Union[str, 'OperatorScope']]] = None,
                 operator_type: Optional[pulumi.Input[Union[str, 'OperatorType']]] = None,
                 repository_url: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 source_control_configuration_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = SourceControlConfigurationArgs.__new__(SourceControlConfigurationArgs)

            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__["cluster_name"] = cluster_name
            if cluster_resource_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_resource_name'")
            __props__.__dict__["cluster_resource_name"] = cluster_resource_name
            if cluster_rp is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_rp'")
            __props__.__dict__["cluster_rp"] = cluster_rp
            __props__.__dict__["enable_helm_operator"] = enable_helm_operator
            __props__.__dict__["helm_operator_properties"] = helm_operator_properties
            __props__.__dict__["operator_instance_name"] = operator_instance_name
            if operator_namespace is None:
                operator_namespace = 'default'
            __props__.__dict__["operator_namespace"] = operator_namespace
            __props__.__dict__["operator_params"] = operator_params
            if operator_scope is None:
                operator_scope = 'cluster'
            __props__.__dict__["operator_scope"] = operator_scope
            __props__.__dict__["operator_type"] = operator_type
            __props__.__dict__["repository_url"] = repository_url
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["source_control_configuration_name"] = source_control_configuration_name
            __props__.__dict__["compliance_status"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["repository_public_key"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:kubernetesconfiguration:SourceControlConfiguration"), pulumi.Alias(type_="azure-native:kubernetesconfiguration/v20200701preview:SourceControlConfiguration"), pulumi.Alias(type_="azure-native:kubernetesconfiguration/v20201001preview:SourceControlConfiguration"), pulumi.Alias(type_="azure-native:kubernetesconfiguration/v20210301:SourceControlConfiguration"), pulumi.Alias(type_="azure-native:kubernetesconfiguration/v20210501preview:SourceControlConfiguration"), pulumi.Alias(type_="azure-native:kubernetesconfiguration/v20211101preview:SourceControlConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SourceControlConfiguration, __self__).__init__(
            'azure-native:kubernetesconfiguration/v20191101preview:SourceControlConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SourceControlConfiguration':
        """
        Get an existing SourceControlConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SourceControlConfigurationArgs.__new__(SourceControlConfigurationArgs)

        __props__.__dict__["compliance_status"] = None
        __props__.__dict__["enable_helm_operator"] = None
        __props__.__dict__["helm_operator_properties"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["operator_instance_name"] = None
        __props__.__dict__["operator_namespace"] = None
        __props__.__dict__["operator_params"] = None
        __props__.__dict__["operator_scope"] = None
        __props__.__dict__["operator_type"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["repository_public_key"] = None
        __props__.__dict__["repository_url"] = None
        __props__.__dict__["type"] = None
        return SourceControlConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="complianceStatus")
    def compliance_status(self) -> pulumi.Output['outputs.ComplianceStatusResponse']:
        """
        Compliance Status of the Configuration
        """
        return pulumi.get(self, "compliance_status")

    @property
    @pulumi.getter(name="enableHelmOperator")
    def enable_helm_operator(self) -> pulumi.Output[Optional[str]]:
        """
        Option to enable Helm Operator for this git configuration.
        """
        return pulumi.get(self, "enable_helm_operator")

    @property
    @pulumi.getter(name="helmOperatorProperties")
    def helm_operator_properties(self) -> pulumi.Output[Optional['outputs.HelmOperatorPropertiesResponse']]:
        """
        Properties for Helm operator.
        """
        return pulumi.get(self, "helm_operator_properties")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="operatorInstanceName")
    def operator_instance_name(self) -> pulumi.Output[Optional[str]]:
        """
        Instance name of the operator - identifying the specific configuration.
        """
        return pulumi.get(self, "operator_instance_name")

    @property
    @pulumi.getter(name="operatorNamespace")
    def operator_namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace to which this operator is installed to. Maximum of 253 lower case alphanumeric characters, hyphen and period only.
        """
        return pulumi.get(self, "operator_namespace")

    @property
    @pulumi.getter(name="operatorParams")
    def operator_params(self) -> pulumi.Output[Optional[str]]:
        """
        Any Parameters for the Operator instance in string format.
        """
        return pulumi.get(self, "operator_params")

    @property
    @pulumi.getter(name="operatorScope")
    def operator_scope(self) -> pulumi.Output[Optional[str]]:
        """
        Scope at which the operator will be installed.
        """
        return pulumi.get(self, "operator_scope")

    @property
    @pulumi.getter(name="operatorType")
    def operator_type(self) -> pulumi.Output[Optional[str]]:
        """
        Type of the operator
        """
        return pulumi.get(self, "operator_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource provider.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="repositoryPublicKey")
    def repository_public_key(self) -> pulumi.Output[str]:
        """
        Public Key associated with this SourceControl configuration (either generated within the cluster or provided by the user).
        """
        return pulumi.get(self, "repository_public_key")

    @property
    @pulumi.getter(name="repositoryUrl")
    def repository_url(self) -> pulumi.Output[Optional[str]]:
        """
        Url of the SourceControl Repository.
        """
        return pulumi.get(self, "repository_url")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

