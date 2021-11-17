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

__all__ = ['WorkbookArgs', 'Workbook']

@pulumi.input_type
class WorkbookArgs:
    def __init__(__self__, *,
                 category: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 serialized_data: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['WorkbookManagedIdentityArgs']] = None,
                 kind: Optional[pulumi.Input[Union[str, 'Kind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[str]] = None,
                 source_id: Optional[pulumi.Input[str]] = None,
                 storage_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Workbook resource.
        :param pulumi.Input[str] category: Workbook category, as defined by the user at creation time.
        :param pulumi.Input[str] display_name: The user-defined name (display name) of the workbook.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] serialized_data: Configuration of this particular workbook. Configuration data is a string containing valid JSON
        :param pulumi.Input[str] description: The description of the workbook.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] etag: Resource etag
        :param pulumi.Input[str] id: Azure resource Id
        :param pulumi.Input['WorkbookManagedIdentityArgs'] identity: Identity used for BYOS
        :param pulumi.Input[Union[str, 'Kind']] kind: The kind of workbook. Choices are user and shared.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] name: Azure resource name
        :param pulumi.Input[str] resource_name: The name of the Application Insights component resource.
        :param pulumi.Input[str] revision: The unique revision id for this workbook definition
        :param pulumi.Input[str] source_id: ResourceId for a source resource.
        :param pulumi.Input[str] storage_uri: BYOS Storage Account URI
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Azure resource type
        :param pulumi.Input[str] version: Workbook version
        """
        pulumi.set(__self__, "category", category)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "serialized_data", serialized_data)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if revision is not None:
            pulumi.set(__self__, "revision", revision)
        if source_id is not None:
            pulumi.set(__self__, "source_id", source_id)
        if storage_uri is not None:
            pulumi.set(__self__, "storage_uri", storage_uri)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Input[str]:
        """
        Workbook category, as defined by the user at creation time.
        """
        return pulumi.get(self, "category")

    @category.setter
    def category(self, value: pulumi.Input[str]):
        pulumi.set(self, "category", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The user-defined name (display name) of the workbook.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

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
    @pulumi.getter(name="serializedData")
    def serialized_data(self) -> pulumi.Input[str]:
        """
        Configuration of this particular workbook. Configuration data is a string containing valid JSON
        """
        return pulumi.get(self, "serialized_data")

    @serialized_data.setter
    def serialized_data(self, value: pulumi.Input[str]):
        pulumi.set(self, "serialized_data", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the workbook.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource etag
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['WorkbookManagedIdentityArgs']]:
        """
        Identity used for BYOS
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['WorkbookManagedIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[Union[str, 'Kind']]]:
        """
        The kind of workbook. Choices are user and shared.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[Union[str, 'Kind']]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Application Insights component resource.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter
    def revision(self) -> Optional[pulumi.Input[str]]:
        """
        The unique revision id for this workbook definition
        """
        return pulumi.get(self, "revision")

    @revision.setter
    def revision(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "revision", value)

    @property
    @pulumi.getter(name="sourceId")
    def source_id(self) -> Optional[pulumi.Input[str]]:
        """
        ResourceId for a source resource.
        """
        return pulumi.get(self, "source_id")

    @source_id.setter
    def source_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_id", value)

    @property
    @pulumi.getter(name="storageUri")
    def storage_uri(self) -> Optional[pulumi.Input[str]]:
        """
        BYOS Storage Account URI
        """
        return pulumi.get(self, "storage_uri")

    @storage_uri.setter
    def storage_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_uri", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Workbook version
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


class Workbook(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['WorkbookManagedIdentityArgs']]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'Kind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[str]] = None,
                 serialized_data: Optional[pulumi.Input[str]] = None,
                 source_id: Optional[pulumi.Input[str]] = None,
                 storage_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An Application Insights workbook definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] category: Workbook category, as defined by the user at creation time.
        :param pulumi.Input[str] description: The description of the workbook.
        :param pulumi.Input[str] display_name: The user-defined name (display name) of the workbook.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] etag: Resource etag
        :param pulumi.Input[str] id: Azure resource Id
        :param pulumi.Input[pulumi.InputType['WorkbookManagedIdentityArgs']] identity: Identity used for BYOS
        :param pulumi.Input[Union[str, 'Kind']] kind: The kind of workbook. Choices are user and shared.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] name: Azure resource name
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] resource_name_: The name of the Application Insights component resource.
        :param pulumi.Input[str] revision: The unique revision id for this workbook definition
        :param pulumi.Input[str] serialized_data: Configuration of this particular workbook. Configuration data is a string containing valid JSON
        :param pulumi.Input[str] source_id: ResourceId for a source resource.
        :param pulumi.Input[str] storage_uri: BYOS Storage Account URI
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Azure resource type
        :param pulumi.Input[str] version: Workbook version
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WorkbookArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Application Insights workbook definition.

        :param str resource_name: The name of the resource.
        :param WorkbookArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkbookArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['WorkbookManagedIdentityArgs']]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'Kind']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[str]] = None,
                 serialized_data: Optional[pulumi.Input[str]] = None,
                 source_id: Optional[pulumi.Input[str]] = None,
                 storage_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
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
            __props__ = WorkbookArgs.__new__(WorkbookArgs)

            if category is None and not opts.urn:
                raise TypeError("Missing required property 'category'")
            __props__.__dict__["category"] = category
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["etag"] = etag
            __props__.__dict__["id"] = id
            __props__.__dict__["identity"] = identity
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["revision"] = revision
            if serialized_data is None and not opts.urn:
                raise TypeError("Missing required property 'serialized_data'")
            __props__.__dict__["serialized_data"] = serialized_data
            __props__.__dict__["source_id"] = source_id
            __props__.__dict__["storage_uri"] = storage_uri
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
            __props__.__dict__["version"] = version
            __props__.__dict__["system_data"] = None
            __props__.__dict__["time_modified"] = None
            __props__.__dict__["user_id"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:insights:Workbook"), pulumi.Alias(type_="azure-native:insights/v20150501:Workbook"), pulumi.Alias(type_="azure-native:insights/v20180617preview:Workbook"), pulumi.Alias(type_="azure-native:insights/v20201020:Workbook"), pulumi.Alias(type_="azure-native:insights/v20210801:Workbook")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Workbook, __self__).__init__(
            'azure-native:insights/v20210308:Workbook',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Workbook':
        """
        Get an existing Workbook resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WorkbookArgs.__new__(WorkbookArgs)

        __props__.__dict__["category"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["revision"] = None
        __props__.__dict__["serialized_data"] = None
        __props__.__dict__["source_id"] = None
        __props__.__dict__["storage_uri"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["time_modified"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["user_id"] = None
        __props__.__dict__["version"] = None
        return Workbook(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Output[str]:
        """
        Workbook category, as defined by the user at creation time.
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the workbook.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The user-defined name (display name) of the workbook.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource etag
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.WorkbookManagedIdentityResponse']]:
        """
        Identity used for BYOS
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        The kind of workbook. Choices are user and shared.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def revision(self) -> pulumi.Output[Optional[str]]:
        """
        The unique revision id for this workbook definition
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter(name="serializedData")
    def serialized_data(self) -> pulumi.Output[str]:
        """
        Configuration of this particular workbook. Configuration data is a string containing valid JSON
        """
        return pulumi.get(self, "serialized_data")

    @property
    @pulumi.getter(name="sourceId")
    def source_id(self) -> pulumi.Output[Optional[str]]:
        """
        ResourceId for a source resource.
        """
        return pulumi.get(self, "source_id")

    @property
    @pulumi.getter(name="storageUri")
    def storage_uri(self) -> pulumi.Output[Optional[str]]:
        """
        BYOS Storage Account URI
        """
        return pulumi.get(self, "storage_uri")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeModified")
    def time_modified(self) -> pulumi.Output[str]:
        """
        Date and time in UTC of the last modification that was made to this workbook definition.
        """
        return pulumi.get(self, "time_modified")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        Unique user id of the specific user that owns this workbook.
        """
        return pulumi.get(self, "user_id")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        Workbook version
        """
        return pulumi.get(self, "version")

