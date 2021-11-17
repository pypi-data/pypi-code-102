# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ImageVersionArgs', 'ImageVersion']

@pulumi.input_type
class ImageVersionArgs:
    def __init__(__self__, *,
                 base_image: pulumi.Input[str],
                 image_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a ImageVersion resource.
        """
        pulumi.set(__self__, "base_image", base_image)
        pulumi.set(__self__, "image_name", image_name)

    @property
    @pulumi.getter(name="baseImage")
    def base_image(self) -> pulumi.Input[str]:
        return pulumi.get(self, "base_image")

    @base_image.setter
    def base_image(self, value: pulumi.Input[str]):
        pulumi.set(self, "base_image", value)

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "image_name")

    @image_name.setter
    def image_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "image_name", value)


class ImageVersion(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_image: Optional[pulumi.Input[str]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::SageMaker::ImageVersion

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ImageVersionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::SageMaker::ImageVersion

        :param str resource_name: The name of the resource.
        :param ImageVersionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ImageVersionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_image: Optional[pulumi.Input[str]] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ImageVersionArgs.__new__(ImageVersionArgs)

            if base_image is None and not opts.urn:
                raise TypeError("Missing required property 'base_image'")
            __props__.__dict__["base_image"] = base_image
            if image_name is None and not opts.urn:
                raise TypeError("Missing required property 'image_name'")
            __props__.__dict__["image_name"] = image_name
            __props__.__dict__["container_image"] = None
            __props__.__dict__["image_arn"] = None
            __props__.__dict__["image_version_arn"] = None
            __props__.__dict__["version"] = None
        super(ImageVersion, __self__).__init__(
            'aws-native:sagemaker:ImageVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ImageVersion':
        """
        Get an existing ImageVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ImageVersionArgs.__new__(ImageVersionArgs)

        __props__.__dict__["base_image"] = None
        __props__.__dict__["container_image"] = None
        __props__.__dict__["image_arn"] = None
        __props__.__dict__["image_name"] = None
        __props__.__dict__["image_version_arn"] = None
        __props__.__dict__["version"] = None
        return ImageVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="baseImage")
    def base_image(self) -> pulumi.Output[str]:
        return pulumi.get(self, "base_image")

    @property
    @pulumi.getter(name="containerImage")
    def container_image(self) -> pulumi.Output[str]:
        return pulumi.get(self, "container_image")

    @property
    @pulumi.getter(name="imageArn")
    def image_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "image_arn")

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "image_name")

    @property
    @pulumi.getter(name="imageVersionArn")
    def image_version_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "image_version_arn")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        return pulumi.get(self, "version")

