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

__all__ = ['SubscriptionArgs', 'Subscription']

@pulumi.input_type
class SubscriptionArgs:
    def __init__(__self__, *,
                 namespace_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 topic_name: pulumi.Input[str],
                 auto_delete_on_idle: Optional[pulumi.Input[str]] = None,
                 dead_lettering_on_filter_evaluation_exceptions: Optional[pulumi.Input[bool]] = None,
                 dead_lettering_on_message_expiration: Optional[pulumi.Input[bool]] = None,
                 default_message_time_to_live: Optional[pulumi.Input[str]] = None,
                 duplicate_detection_history_time_window: Optional[pulumi.Input[str]] = None,
                 enable_batched_operations: Optional[pulumi.Input[bool]] = None,
                 forward_dead_lettered_messages_to: Optional[pulumi.Input[str]] = None,
                 forward_to: Optional[pulumi.Input[str]] = None,
                 lock_duration: Optional[pulumi.Input[str]] = None,
                 max_delivery_count: Optional[pulumi.Input[int]] = None,
                 requires_session: Optional[pulumi.Input[bool]] = None,
                 status: Optional[pulumi.Input['EntityStatus']] = None,
                 subscription_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Subscription resource.
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input[str] topic_name: The topic name.
        :param pulumi.Input[str] auto_delete_on_idle: ISO 8061 timeSpan idle interval after which the topic is automatically deleted. The minimum duration is 5 minutes.
        :param pulumi.Input[bool] dead_lettering_on_filter_evaluation_exceptions: Value that indicates whether a subscription has dead letter support on filter evaluation exceptions.
        :param pulumi.Input[bool] dead_lettering_on_message_expiration: Value that indicates whether a subscription has dead letter support when a message expires.
        :param pulumi.Input[str] default_message_time_to_live: ISO 8061 Default message timespan to live value. This is the duration after which the message expires, starting from when the message is sent to Service Bus. This is the default value used when TimeToLive is not set on a message itself.
        :param pulumi.Input[str] duplicate_detection_history_time_window: ISO 8601 timeSpan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
        :param pulumi.Input[bool] enable_batched_operations: Value that indicates whether server-side batched operations are enabled.
        :param pulumi.Input[str] forward_dead_lettered_messages_to: Queue/Topic name to forward the Dead Letter message
        :param pulumi.Input[str] forward_to: Queue/Topic name to forward the messages
        :param pulumi.Input[str] lock_duration: ISO 8061 lock duration timespan for the subscription. The default value is 1 minute.
        :param pulumi.Input[int] max_delivery_count: Number of maximum deliveries.
        :param pulumi.Input[bool] requires_session: Value indicating if a subscription supports the concept of sessions.
        :param pulumi.Input['EntityStatus'] status: Enumerates the possible values for the status of a messaging entity.
        :param pulumi.Input[str] subscription_name: The subscription name.
        """
        pulumi.set(__self__, "namespace_name", namespace_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "topic_name", topic_name)
        if auto_delete_on_idle is not None:
            pulumi.set(__self__, "auto_delete_on_idle", auto_delete_on_idle)
        if dead_lettering_on_filter_evaluation_exceptions is not None:
            pulumi.set(__self__, "dead_lettering_on_filter_evaluation_exceptions", dead_lettering_on_filter_evaluation_exceptions)
        if dead_lettering_on_message_expiration is not None:
            pulumi.set(__self__, "dead_lettering_on_message_expiration", dead_lettering_on_message_expiration)
        if default_message_time_to_live is not None:
            pulumi.set(__self__, "default_message_time_to_live", default_message_time_to_live)
        if duplicate_detection_history_time_window is not None:
            pulumi.set(__self__, "duplicate_detection_history_time_window", duplicate_detection_history_time_window)
        if enable_batched_operations is not None:
            pulumi.set(__self__, "enable_batched_operations", enable_batched_operations)
        if forward_dead_lettered_messages_to is not None:
            pulumi.set(__self__, "forward_dead_lettered_messages_to", forward_dead_lettered_messages_to)
        if forward_to is not None:
            pulumi.set(__self__, "forward_to", forward_to)
        if lock_duration is not None:
            pulumi.set(__self__, "lock_duration", lock_duration)
        if max_delivery_count is not None:
            pulumi.set(__self__, "max_delivery_count", max_delivery_count)
        if requires_session is not None:
            pulumi.set(__self__, "requires_session", requires_session)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if subscription_name is not None:
            pulumi.set(__self__, "subscription_name", subscription_name)

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> pulumi.Input[str]:
        """
        The namespace name
        """
        return pulumi.get(self, "namespace_name")

    @namespace_name.setter
    def namespace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "namespace_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the Resource group within the Azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="topicName")
    def topic_name(self) -> pulumi.Input[str]:
        """
        The topic name.
        """
        return pulumi.get(self, "topic_name")

    @topic_name.setter
    def topic_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "topic_name", value)

    @property
    @pulumi.getter(name="autoDeleteOnIdle")
    def auto_delete_on_idle(self) -> Optional[pulumi.Input[str]]:
        """
        ISO 8061 timeSpan idle interval after which the topic is automatically deleted. The minimum duration is 5 minutes.
        """
        return pulumi.get(self, "auto_delete_on_idle")

    @auto_delete_on_idle.setter
    def auto_delete_on_idle(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auto_delete_on_idle", value)

    @property
    @pulumi.getter(name="deadLetteringOnFilterEvaluationExceptions")
    def dead_lettering_on_filter_evaluation_exceptions(self) -> Optional[pulumi.Input[bool]]:
        """
        Value that indicates whether a subscription has dead letter support on filter evaluation exceptions.
        """
        return pulumi.get(self, "dead_lettering_on_filter_evaluation_exceptions")

    @dead_lettering_on_filter_evaluation_exceptions.setter
    def dead_lettering_on_filter_evaluation_exceptions(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dead_lettering_on_filter_evaluation_exceptions", value)

    @property
    @pulumi.getter(name="deadLetteringOnMessageExpiration")
    def dead_lettering_on_message_expiration(self) -> Optional[pulumi.Input[bool]]:
        """
        Value that indicates whether a subscription has dead letter support when a message expires.
        """
        return pulumi.get(self, "dead_lettering_on_message_expiration")

    @dead_lettering_on_message_expiration.setter
    def dead_lettering_on_message_expiration(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dead_lettering_on_message_expiration", value)

    @property
    @pulumi.getter(name="defaultMessageTimeToLive")
    def default_message_time_to_live(self) -> Optional[pulumi.Input[str]]:
        """
        ISO 8061 Default message timespan to live value. This is the duration after which the message expires, starting from when the message is sent to Service Bus. This is the default value used when TimeToLive is not set on a message itself.
        """
        return pulumi.get(self, "default_message_time_to_live")

    @default_message_time_to_live.setter
    def default_message_time_to_live(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_message_time_to_live", value)

    @property
    @pulumi.getter(name="duplicateDetectionHistoryTimeWindow")
    def duplicate_detection_history_time_window(self) -> Optional[pulumi.Input[str]]:
        """
        ISO 8601 timeSpan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
        """
        return pulumi.get(self, "duplicate_detection_history_time_window")

    @duplicate_detection_history_time_window.setter
    def duplicate_detection_history_time_window(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "duplicate_detection_history_time_window", value)

    @property
    @pulumi.getter(name="enableBatchedOperations")
    def enable_batched_operations(self) -> Optional[pulumi.Input[bool]]:
        """
        Value that indicates whether server-side batched operations are enabled.
        """
        return pulumi.get(self, "enable_batched_operations")

    @enable_batched_operations.setter
    def enable_batched_operations(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_batched_operations", value)

    @property
    @pulumi.getter(name="forwardDeadLetteredMessagesTo")
    def forward_dead_lettered_messages_to(self) -> Optional[pulumi.Input[str]]:
        """
        Queue/Topic name to forward the Dead Letter message
        """
        return pulumi.get(self, "forward_dead_lettered_messages_to")

    @forward_dead_lettered_messages_to.setter
    def forward_dead_lettered_messages_to(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "forward_dead_lettered_messages_to", value)

    @property
    @pulumi.getter(name="forwardTo")
    def forward_to(self) -> Optional[pulumi.Input[str]]:
        """
        Queue/Topic name to forward the messages
        """
        return pulumi.get(self, "forward_to")

    @forward_to.setter
    def forward_to(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "forward_to", value)

    @property
    @pulumi.getter(name="lockDuration")
    def lock_duration(self) -> Optional[pulumi.Input[str]]:
        """
        ISO 8061 lock duration timespan for the subscription. The default value is 1 minute.
        """
        return pulumi.get(self, "lock_duration")

    @lock_duration.setter
    def lock_duration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lock_duration", value)

    @property
    @pulumi.getter(name="maxDeliveryCount")
    def max_delivery_count(self) -> Optional[pulumi.Input[int]]:
        """
        Number of maximum deliveries.
        """
        return pulumi.get(self, "max_delivery_count")

    @max_delivery_count.setter
    def max_delivery_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_delivery_count", value)

    @property
    @pulumi.getter(name="requiresSession")
    def requires_session(self) -> Optional[pulumi.Input[bool]]:
        """
        Value indicating if a subscription supports the concept of sessions.
        """
        return pulumi.get(self, "requires_session")

    @requires_session.setter
    def requires_session(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "requires_session", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input['EntityStatus']]:
        """
        Enumerates the possible values for the status of a messaging entity.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input['EntityStatus']]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="subscriptionName")
    def subscription_name(self) -> Optional[pulumi.Input[str]]:
        """
        The subscription name.
        """
        return pulumi.get(self, "subscription_name")

    @subscription_name.setter
    def subscription_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscription_name", value)


class Subscription(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_delete_on_idle: Optional[pulumi.Input[str]] = None,
                 dead_lettering_on_filter_evaluation_exceptions: Optional[pulumi.Input[bool]] = None,
                 dead_lettering_on_message_expiration: Optional[pulumi.Input[bool]] = None,
                 default_message_time_to_live: Optional[pulumi.Input[str]] = None,
                 duplicate_detection_history_time_window: Optional[pulumi.Input[str]] = None,
                 enable_batched_operations: Optional[pulumi.Input[bool]] = None,
                 forward_dead_lettered_messages_to: Optional[pulumi.Input[str]] = None,
                 forward_to: Optional[pulumi.Input[str]] = None,
                 lock_duration: Optional[pulumi.Input[str]] = None,
                 max_delivery_count: Optional[pulumi.Input[int]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 requires_session: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['EntityStatus']] = None,
                 subscription_name: Optional[pulumi.Input[str]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Description of subscription resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] auto_delete_on_idle: ISO 8061 timeSpan idle interval after which the topic is automatically deleted. The minimum duration is 5 minutes.
        :param pulumi.Input[bool] dead_lettering_on_filter_evaluation_exceptions: Value that indicates whether a subscription has dead letter support on filter evaluation exceptions.
        :param pulumi.Input[bool] dead_lettering_on_message_expiration: Value that indicates whether a subscription has dead letter support when a message expires.
        :param pulumi.Input[str] default_message_time_to_live: ISO 8061 Default message timespan to live value. This is the duration after which the message expires, starting from when the message is sent to Service Bus. This is the default value used when TimeToLive is not set on a message itself.
        :param pulumi.Input[str] duplicate_detection_history_time_window: ISO 8601 timeSpan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
        :param pulumi.Input[bool] enable_batched_operations: Value that indicates whether server-side batched operations are enabled.
        :param pulumi.Input[str] forward_dead_lettered_messages_to: Queue/Topic name to forward the Dead Letter message
        :param pulumi.Input[str] forward_to: Queue/Topic name to forward the messages
        :param pulumi.Input[str] lock_duration: ISO 8061 lock duration timespan for the subscription. The default value is 1 minute.
        :param pulumi.Input[int] max_delivery_count: Number of maximum deliveries.
        :param pulumi.Input[str] namespace_name: The namespace name
        :param pulumi.Input[bool] requires_session: Value indicating if a subscription supports the concept of sessions.
        :param pulumi.Input[str] resource_group_name: Name of the Resource group within the Azure subscription.
        :param pulumi.Input['EntityStatus'] status: Enumerates the possible values for the status of a messaging entity.
        :param pulumi.Input[str] subscription_name: The subscription name.
        :param pulumi.Input[str] topic_name: The topic name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SubscriptionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Description of subscription resource.

        :param str resource_name: The name of the resource.
        :param SubscriptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SubscriptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_delete_on_idle: Optional[pulumi.Input[str]] = None,
                 dead_lettering_on_filter_evaluation_exceptions: Optional[pulumi.Input[bool]] = None,
                 dead_lettering_on_message_expiration: Optional[pulumi.Input[bool]] = None,
                 default_message_time_to_live: Optional[pulumi.Input[str]] = None,
                 duplicate_detection_history_time_window: Optional[pulumi.Input[str]] = None,
                 enable_batched_operations: Optional[pulumi.Input[bool]] = None,
                 forward_dead_lettered_messages_to: Optional[pulumi.Input[str]] = None,
                 forward_to: Optional[pulumi.Input[str]] = None,
                 lock_duration: Optional[pulumi.Input[str]] = None,
                 max_delivery_count: Optional[pulumi.Input[int]] = None,
                 namespace_name: Optional[pulumi.Input[str]] = None,
                 requires_session: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input['EntityStatus']] = None,
                 subscription_name: Optional[pulumi.Input[str]] = None,
                 topic_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = SubscriptionArgs.__new__(SubscriptionArgs)

            __props__.__dict__["auto_delete_on_idle"] = auto_delete_on_idle
            __props__.__dict__["dead_lettering_on_filter_evaluation_exceptions"] = dead_lettering_on_filter_evaluation_exceptions
            __props__.__dict__["dead_lettering_on_message_expiration"] = dead_lettering_on_message_expiration
            __props__.__dict__["default_message_time_to_live"] = default_message_time_to_live
            __props__.__dict__["duplicate_detection_history_time_window"] = duplicate_detection_history_time_window
            __props__.__dict__["enable_batched_operations"] = enable_batched_operations
            __props__.__dict__["forward_dead_lettered_messages_to"] = forward_dead_lettered_messages_to
            __props__.__dict__["forward_to"] = forward_to
            __props__.__dict__["lock_duration"] = lock_duration
            __props__.__dict__["max_delivery_count"] = max_delivery_count
            if namespace_name is None and not opts.urn:
                raise TypeError("Missing required property 'namespace_name'")
            __props__.__dict__["namespace_name"] = namespace_name
            __props__.__dict__["requires_session"] = requires_session
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["status"] = status
            __props__.__dict__["subscription_name"] = subscription_name
            if topic_name is None and not opts.urn:
                raise TypeError("Missing required property 'topic_name'")
            __props__.__dict__["topic_name"] = topic_name
            __props__.__dict__["accessed_at"] = None
            __props__.__dict__["count_details"] = None
            __props__.__dict__["created_at"] = None
            __props__.__dict__["message_count"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["updated_at"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:servicebus:Subscription"), pulumi.Alias(type_="azure-native:servicebus/v20140901:Subscription"), pulumi.Alias(type_="azure-native:servicebus/v20150801:Subscription"), pulumi.Alias(type_="azure-native:servicebus/v20180101preview:Subscription"), pulumi.Alias(type_="azure-native:servicebus/v20210101preview:Subscription"), pulumi.Alias(type_="azure-native:servicebus/v20210601preview:Subscription")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Subscription, __self__).__init__(
            'azure-native:servicebus/v20170401:Subscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Subscription':
        """
        Get an existing Subscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SubscriptionArgs.__new__(SubscriptionArgs)

        __props__.__dict__["accessed_at"] = None
        __props__.__dict__["auto_delete_on_idle"] = None
        __props__.__dict__["count_details"] = None
        __props__.__dict__["created_at"] = None
        __props__.__dict__["dead_lettering_on_filter_evaluation_exceptions"] = None
        __props__.__dict__["dead_lettering_on_message_expiration"] = None
        __props__.__dict__["default_message_time_to_live"] = None
        __props__.__dict__["duplicate_detection_history_time_window"] = None
        __props__.__dict__["enable_batched_operations"] = None
        __props__.__dict__["forward_dead_lettered_messages_to"] = None
        __props__.__dict__["forward_to"] = None
        __props__.__dict__["lock_duration"] = None
        __props__.__dict__["max_delivery_count"] = None
        __props__.__dict__["message_count"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["requires_session"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["updated_at"] = None
        return Subscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessedAt")
    def accessed_at(self) -> pulumi.Output[str]:
        """
        Last time there was a receive request to this subscription.
        """
        return pulumi.get(self, "accessed_at")

    @property
    @pulumi.getter(name="autoDeleteOnIdle")
    def auto_delete_on_idle(self) -> pulumi.Output[Optional[str]]:
        """
        ISO 8061 timeSpan idle interval after which the topic is automatically deleted. The minimum duration is 5 minutes.
        """
        return pulumi.get(self, "auto_delete_on_idle")

    @property
    @pulumi.getter(name="countDetails")
    def count_details(self) -> pulumi.Output['outputs.MessageCountDetailsResponse']:
        """
        Message count details
        """
        return pulumi.get(self, "count_details")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Exact time the message was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="deadLetteringOnFilterEvaluationExceptions")
    def dead_lettering_on_filter_evaluation_exceptions(self) -> pulumi.Output[Optional[bool]]:
        """
        Value that indicates whether a subscription has dead letter support on filter evaluation exceptions.
        """
        return pulumi.get(self, "dead_lettering_on_filter_evaluation_exceptions")

    @property
    @pulumi.getter(name="deadLetteringOnMessageExpiration")
    def dead_lettering_on_message_expiration(self) -> pulumi.Output[Optional[bool]]:
        """
        Value that indicates whether a subscription has dead letter support when a message expires.
        """
        return pulumi.get(self, "dead_lettering_on_message_expiration")

    @property
    @pulumi.getter(name="defaultMessageTimeToLive")
    def default_message_time_to_live(self) -> pulumi.Output[Optional[str]]:
        """
        ISO 8061 Default message timespan to live value. This is the duration after which the message expires, starting from when the message is sent to Service Bus. This is the default value used when TimeToLive is not set on a message itself.
        """
        return pulumi.get(self, "default_message_time_to_live")

    @property
    @pulumi.getter(name="duplicateDetectionHistoryTimeWindow")
    def duplicate_detection_history_time_window(self) -> pulumi.Output[Optional[str]]:
        """
        ISO 8601 timeSpan structure that defines the duration of the duplicate detection history. The default value is 10 minutes.
        """
        return pulumi.get(self, "duplicate_detection_history_time_window")

    @property
    @pulumi.getter(name="enableBatchedOperations")
    def enable_batched_operations(self) -> pulumi.Output[Optional[bool]]:
        """
        Value that indicates whether server-side batched operations are enabled.
        """
        return pulumi.get(self, "enable_batched_operations")

    @property
    @pulumi.getter(name="forwardDeadLetteredMessagesTo")
    def forward_dead_lettered_messages_to(self) -> pulumi.Output[Optional[str]]:
        """
        Queue/Topic name to forward the Dead Letter message
        """
        return pulumi.get(self, "forward_dead_lettered_messages_to")

    @property
    @pulumi.getter(name="forwardTo")
    def forward_to(self) -> pulumi.Output[Optional[str]]:
        """
        Queue/Topic name to forward the messages
        """
        return pulumi.get(self, "forward_to")

    @property
    @pulumi.getter(name="lockDuration")
    def lock_duration(self) -> pulumi.Output[Optional[str]]:
        """
        ISO 8061 lock duration timespan for the subscription. The default value is 1 minute.
        """
        return pulumi.get(self, "lock_duration")

    @property
    @pulumi.getter(name="maxDeliveryCount")
    def max_delivery_count(self) -> pulumi.Output[Optional[int]]:
        """
        Number of maximum deliveries.
        """
        return pulumi.get(self, "max_delivery_count")

    @property
    @pulumi.getter(name="messageCount")
    def message_count(self) -> pulumi.Output[float]:
        """
        Number of messages.
        """
        return pulumi.get(self, "message_count")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="requiresSession")
    def requires_session(self) -> pulumi.Output[Optional[bool]]:
        """
        Value indicating if a subscription supports the concept of sessions.
        """
        return pulumi.get(self, "requires_session")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Enumerates the possible values for the status of a messaging entity.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The exact time the message was updated.
        """
        return pulumi.get(self, "updated_at")

