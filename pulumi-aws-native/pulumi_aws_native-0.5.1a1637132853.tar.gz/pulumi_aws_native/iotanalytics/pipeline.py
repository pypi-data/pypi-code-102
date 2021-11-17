# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['PipelineArgs', 'Pipeline']

@pulumi.input_type
class PipelineArgs:
    def __init__(__self__, *,
                 pipeline_activities: pulumi.Input[Sequence[pulumi.Input['PipelineActivityArgs']]],
                 pipeline_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['PipelineTagArgs']]]] = None):
        """
        The set of arguments for constructing a Pipeline resource.
        """
        pulumi.set(__self__, "pipeline_activities", pipeline_activities)
        if pipeline_name is not None:
            pulumi.set(__self__, "pipeline_name", pipeline_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="pipelineActivities")
    def pipeline_activities(self) -> pulumi.Input[Sequence[pulumi.Input['PipelineActivityArgs']]]:
        return pulumi.get(self, "pipeline_activities")

    @pipeline_activities.setter
    def pipeline_activities(self, value: pulumi.Input[Sequence[pulumi.Input['PipelineActivityArgs']]]):
        pulumi.set(self, "pipeline_activities", value)

    @property
    @pulumi.getter(name="pipelineName")
    def pipeline_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "pipeline_name")

    @pipeline_name.setter
    def pipeline_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pipeline_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PipelineTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PipelineTagArgs']]]]):
        pulumi.set(self, "tags", value)


warnings.warn("""Pipeline is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Pipeline(pulumi.CustomResource):
    warnings.warn("""Pipeline is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 pipeline_activities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PipelineActivityArgs']]]]] = None,
                 pipeline_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PipelineTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::IoTAnalytics::Pipeline

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PipelineArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::IoTAnalytics::Pipeline

        :param str resource_name: The name of the resource.
        :param PipelineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PipelineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 pipeline_activities: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PipelineActivityArgs']]]]] = None,
                 pipeline_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PipelineTagArgs']]]]] = None,
                 __props__=None):
        pulumi.log.warn("""Pipeline is deprecated: Pipeline is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PipelineArgs.__new__(PipelineArgs)

            if pipeline_activities is None and not opts.urn:
                raise TypeError("Missing required property 'pipeline_activities'")
            __props__.__dict__["pipeline_activities"] = pipeline_activities
            __props__.__dict__["pipeline_name"] = pipeline_name
            __props__.__dict__["tags"] = tags
        super(Pipeline, __self__).__init__(
            'aws-native:iotanalytics:Pipeline',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Pipeline':
        """
        Get an existing Pipeline resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PipelineArgs.__new__(PipelineArgs)

        __props__.__dict__["pipeline_activities"] = None
        __props__.__dict__["pipeline_name"] = None
        __props__.__dict__["tags"] = None
        return Pipeline(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="pipelineActivities")
    def pipeline_activities(self) -> pulumi.Output[Sequence['outputs.PipelineActivity']]:
        return pulumi.get(self, "pipeline_activities")

    @property
    @pulumi.getter(name="pipelineName")
    def pipeline_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "pipeline_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.PipelineTag']]]:
        return pulumi.get(self, "tags")

