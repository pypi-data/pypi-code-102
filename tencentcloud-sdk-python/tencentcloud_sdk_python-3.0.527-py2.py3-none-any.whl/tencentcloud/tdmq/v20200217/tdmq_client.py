# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.abstract_client import AbstractClient
from tencentcloud.tdmq.v20200217 import models


class TdmqClient(AbstractClient):
    _apiVersion = '2020-02-17'
    _endpoint = 'tdmq.tencentcloudapi.com'
    _service = 'tdmq'


    def AcknowledgeMessage(self, request):
        """根据提供的 MessageID 确认指定 topic 中的消息

        :param request: Request instance for AcknowledgeMessage.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.AcknowledgeMessageRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.AcknowledgeMessageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("AcknowledgeMessage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.AcknowledgeMessageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ClearCmqQueue(self, request):
        """清空cmq消息队列中的消息

        :param request: Request instance for ClearCmqQueue.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ClearCmqQueueRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ClearCmqQueueResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ClearCmqQueue", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ClearCmqQueueResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ClearCmqSubscriptionFilterTags(self, request):
        """清空订阅者消息标签

        :param request: Request instance for ClearCmqSubscriptionFilterTags.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ClearCmqSubscriptionFilterTagsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ClearCmqSubscriptionFilterTagsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ClearCmqSubscriptionFilterTags", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ClearCmqSubscriptionFilterTagsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCluster(self, request):
        """创建用户的集群

        :param request: Request instance for CreateCluster.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateClusterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateClusterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCmqQueue(self, request):
        """创建cmq队列接口

        :param request: Request instance for CreateCmqQueue.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateCmqQueueRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateCmqQueueResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCmqQueue", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCmqQueueResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCmqSubscribe(self, request):
        """创建cmq订阅接口

        :param request: Request instance for CreateCmqSubscribe.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateCmqSubscribeRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateCmqSubscribeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCmqSubscribe", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCmqSubscribeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateCmqTopic(self, request):
        """创建cmq主题

        :param request: Request instance for CreateCmqTopic.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateCmqTopicRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateCmqTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateCmqTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateCmqTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateEnvironment(self, request):
        """用于在用户账户下创建消息队列 Tdmq 命名空间

        :param request: Request instance for CreateEnvironment.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateEnvironmentRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateEnvironmentResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateEnvironment", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateEnvironmentResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateEnvironmentRole(self, request):
        """创建环境角色授权

        :param request: Request instance for CreateEnvironmentRole.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateEnvironmentRoleRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateEnvironmentRoleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateEnvironmentRole", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateEnvironmentRoleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateRocketMQCluster(self, request):
        """此接口用于创建一个RocketMQ集群

        :param request: Request instance for CreateRocketMQCluster.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQClusterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRocketMQCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRocketMQClusterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateRocketMQGroup(self, request):
        """创建RocketMQ消费组

        :param request: Request instance for CreateRocketMQGroup.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQGroupRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRocketMQGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRocketMQGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateRocketMQNamespace(self, request):
        """创建RocketMQ命名空间

        :param request: Request instance for CreateRocketMQNamespace.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQNamespaceRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQNamespaceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRocketMQNamespace", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRocketMQNamespaceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateRocketMQTopic(self, request):
        """创建RocketMQ主题

        :param request: Request instance for CreateRocketMQTopic.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQTopicRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateRocketMQTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRocketMQTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRocketMQTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateRole(self, request):
        """创建角色

        :param request: Request instance for CreateRole.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateRoleRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateRoleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateRole", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateRoleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateSubscription(self, request):
        """创建一个主题的订阅关系

        :param request: Request instance for CreateSubscription.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateSubscriptionRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateSubscriptionResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateSubscription", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateSubscriptionResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def CreateTopic(self, request):
        """新增指定分区、类型的消息主题

        :param request: Request instance for CreateTopic.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.CreateTopicRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.CreateTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("CreateTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.CreateTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCluster(self, request):
        """删除集群

        :param request: Request instance for DeleteCluster.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteClusterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteClusterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCmqQueue(self, request):
        """删除cmq队列

        :param request: Request instance for DeleteCmqQueue.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteCmqQueueRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteCmqQueueResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCmqQueue", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCmqQueueResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCmqSubscribe(self, request):
        """删除cmq订阅

        :param request: Request instance for DeleteCmqSubscribe.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteCmqSubscribeRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteCmqSubscribeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCmqSubscribe", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCmqSubscribeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteCmqTopic(self, request):
        """删除cmq主题

        :param request: Request instance for DeleteCmqTopic.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteCmqTopicRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteCmqTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteCmqTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteCmqTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteEnvironmentRoles(self, request):
        """删除环境角色授权。

        :param request: Request instance for DeleteEnvironmentRoles.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteEnvironmentRolesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteEnvironmentRolesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteEnvironmentRoles", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteEnvironmentRolesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteEnvironments(self, request):
        """批量删除租户下的命名空间

        :param request: Request instance for DeleteEnvironments.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteEnvironmentsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteEnvironmentsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteEnvironments", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteEnvironmentsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteRocketMQCluster(self, request):
        """删除RocketMQ集群

        :param request: Request instance for DeleteRocketMQCluster.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQClusterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRocketMQCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRocketMQClusterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteRocketMQGroup(self, request):
        """删除RocketMQ消费组

        :param request: Request instance for DeleteRocketMQGroup.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQGroupRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRocketMQGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRocketMQGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteRocketMQNamespace(self, request):
        """删除RocketMQ命名空间

        :param request: Request instance for DeleteRocketMQNamespace.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQNamespaceRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQNamespaceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRocketMQNamespace", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRocketMQNamespaceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteRocketMQTopic(self, request):
        """删除RocketMQ主题

        :param request: Request instance for DeleteRocketMQTopic.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQTopicRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteRocketMQTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRocketMQTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRocketMQTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteRoles(self, request):
        """删除角色，支持批量。

        :param request: Request instance for DeleteRoles.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteRolesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteRolesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteRoles", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteRolesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteSubscriptions(self, request):
        """删除订阅关系

        :param request: Request instance for DeleteSubscriptions.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteSubscriptionsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteSubscriptionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteSubscriptions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteSubscriptionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DeleteTopics(self, request):
        """批量删除topics

        :param request: Request instance for DeleteTopics.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DeleteTopicsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DeleteTopicsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DeleteTopics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DeleteTopicsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBindClusters(self, request):
        """获取用户绑定的专享集群列表

        :param request: Request instance for DescribeBindClusters.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeBindClustersRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeBindClustersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBindClusters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBindClustersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeBindVpcs(self, request):
        """获取租户VPC绑定关系

        :param request: Request instance for DescribeBindVpcs.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeBindVpcsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeBindVpcsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeBindVpcs", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeBindVpcsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeClusterDetail(self, request):
        """获取集群的详细信息

        :param request: Request instance for DescribeClusterDetail.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeClusterDetailRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeClusterDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusterDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClusterDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeClusters(self, request):
        """获取集群列表

        :param request: Request instance for DescribeClusters.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeClustersRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeClustersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeClusters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeClustersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCmqDeadLetterSourceQueues(self, request):
        """枚举cmq死信队列源队列

        :param request: Request instance for DescribeCmqDeadLetterSourceQueues.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqDeadLetterSourceQueuesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqDeadLetterSourceQueuesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCmqDeadLetterSourceQueues", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCmqDeadLetterSourceQueuesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCmqQueueDetail(self, request):
        """查询cmq队列详情

        :param request: Request instance for DescribeCmqQueueDetail.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqQueueDetailRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqQueueDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCmqQueueDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCmqQueueDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCmqQueues(self, request):
        """查询cmq全量队列

        :param request: Request instance for DescribeCmqQueues.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqQueuesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqQueuesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCmqQueues", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCmqQueuesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCmqSubscriptionDetail(self, request):
        """查询cmq订阅详情

        :param request: Request instance for DescribeCmqSubscriptionDetail.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqSubscriptionDetailRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqSubscriptionDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCmqSubscriptionDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCmqSubscriptionDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCmqTopicDetail(self, request):
        """查询cmq主题详情

        :param request: Request instance for DescribeCmqTopicDetail.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqTopicDetailRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqTopicDetailResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCmqTopicDetail", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCmqTopicDetailResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeCmqTopics(self, request):
        """枚举cmq全量主题

        :param request: Request instance for DescribeCmqTopics.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqTopicsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeCmqTopicsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeCmqTopics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeCmqTopicsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeEnvironmentAttributes(self, request):
        """获取指定命名空间的属性

        :param request: Request instance for DescribeEnvironmentAttributes.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeEnvironmentAttributesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeEnvironmentAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeEnvironmentAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeEnvironmentAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeEnvironmentRoles(self, request):
        """获取命名空间角色列表

        :param request: Request instance for DescribeEnvironmentRoles.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeEnvironmentRolesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeEnvironmentRolesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeEnvironmentRoles", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeEnvironmentRolesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeEnvironments(self, request):
        """获取租户下命名空间列表

        :param request: Request instance for DescribeEnvironments.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeEnvironmentsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeEnvironmentsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeEnvironments", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeEnvironmentsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNamespaceBundlesOpt(self, request):
        """运营端获取命名空间bundle列表

        :param request: Request instance for DescribeNamespaceBundlesOpt.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeNamespaceBundlesOptRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeNamespaceBundlesOptResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeNamespaceBundlesOpt", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNamespaceBundlesOptResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeNodeHealthOpt(self, request):
        """运营端获节点健康状态

        :param request: Request instance for DescribeNodeHealthOpt.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeNodeHealthOptRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeNodeHealthOptResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeNodeHealthOpt", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeNodeHealthOptResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeProducers(self, request):
        """获取生产者列表，仅显示在线的生产者

        :param request: Request instance for DescribeProducers.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeProducersRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeProducersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeProducers", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeProducersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRocketMQCluster(self, request):
        """获取单个RocketMQ集群信息

        :param request: Request instance for DescribeRocketMQCluster.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQClusterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRocketMQCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRocketMQClusterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRocketMQClusters(self, request):
        """获取RocketMQ集群列表

        :param request: Request instance for DescribeRocketMQClusters.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQClustersRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQClustersResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRocketMQClusters", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRocketMQClustersResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRocketMQGroups(self, request):
        """获取RocketMQ消费组列表

        :param request: Request instance for DescribeRocketMQGroups.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQGroupsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQGroupsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRocketMQGroups", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRocketMQGroupsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRocketMQNamespaces(self, request):
        """获取RocketMQ命名空间列表

        :param request: Request instance for DescribeRocketMQNamespaces.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQNamespacesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQNamespacesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRocketMQNamespaces", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRocketMQNamespacesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRocketMQTopics(self, request):
        """获取RocketMQ主题列表

        :param request: Request instance for DescribeRocketMQTopics.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQTopicsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeRocketMQTopicsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRocketMQTopics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRocketMQTopicsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeRoles(self, request):
        """获取角色列表

        :param request: Request instance for DescribeRoles.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeRolesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeRolesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeRoles", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeRolesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeSubscriptions(self, request):
        """查询指定环境和主题下的订阅者列表

        :param request: Request instance for DescribeSubscriptions.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeSubscriptionsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeSubscriptionsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeSubscriptions", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeSubscriptionsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def DescribeTopics(self, request):
        """获取环境下主题列表

        :param request: Request instance for DescribeTopics.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.DescribeTopicsRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.DescribeTopicsResponse`

        """
        try:
            params = request._serialize()
            body = self.call("DescribeTopics", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.DescribeTopicsResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCluster(self, request):
        """更新集群信息

        :param request: Request instance for ModifyCluster.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyClusterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyClusterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCmqQueueAttribute(self, request):
        """修改cmq队列属性

        :param request: Request instance for ModifyCmqQueueAttribute.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyCmqQueueAttributeRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyCmqQueueAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyCmqQueueAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyCmqQueueAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCmqSubscriptionAttribute(self, request):
        """修改cmq订阅属性

        :param request: Request instance for ModifyCmqSubscriptionAttribute.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyCmqSubscriptionAttributeRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyCmqSubscriptionAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyCmqSubscriptionAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyCmqSubscriptionAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyCmqTopicAttribute(self, request):
        """修改cmq主题属性

        :param request: Request instance for ModifyCmqTopicAttribute.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyCmqTopicAttributeRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyCmqTopicAttributeResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyCmqTopicAttribute", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyCmqTopicAttributeResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyEnvironmentAttributes(self, request):
        """修改指定命名空间的属性值

        :param request: Request instance for ModifyEnvironmentAttributes.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyEnvironmentAttributesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyEnvironmentAttributesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyEnvironmentAttributes", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyEnvironmentAttributesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyEnvironmentRole(self, request):
        """修改环境角色授权。

        :param request: Request instance for ModifyEnvironmentRole.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyEnvironmentRoleRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyEnvironmentRoleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyEnvironmentRole", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyEnvironmentRoleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRocketMQCluster(self, request):
        """更新RocketMQ集群信息

        :param request: Request instance for ModifyRocketMQCluster.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQClusterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQClusterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRocketMQCluster", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRocketMQClusterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRocketMQGroup(self, request):
        """更新RocketMQ消费组信息

        :param request: Request instance for ModifyRocketMQGroup.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQGroupRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQGroupResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRocketMQGroup", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRocketMQGroupResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRocketMQNamespace(self, request):
        """更新RocketMQ命名空间

        :param request: Request instance for ModifyRocketMQNamespace.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQNamespaceRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQNamespaceResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRocketMQNamespace", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRocketMQNamespaceResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRocketMQTopic(self, request):
        """更新RocketMQ主题信息

        :param request: Request instance for ModifyRocketMQTopic.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQTopicRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyRocketMQTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRocketMQTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRocketMQTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyRole(self, request):
        """角色修改

        :param request: Request instance for ModifyRole.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyRoleRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyRoleResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyRole", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyRoleResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ModifyTopic(self, request):
        """修改主题备注和分区数

        :param request: Request instance for ModifyTopic.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ModifyTopicRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ModifyTopicResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ModifyTopic", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ModifyTopicResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def PublishCmqMsg(self, request):
        """发送cmq主题消息

        :param request: Request instance for PublishCmqMsg.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.PublishCmqMsgRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.PublishCmqMsgResponse`

        """
        try:
            params = request._serialize()
            body = self.call("PublishCmqMsg", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.PublishCmqMsgResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ReceiveMessage(self, request):
        """接收发送到指定 topic 中的消息

        :param request: Request instance for ReceiveMessage.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ReceiveMessageRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ReceiveMessageResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ReceiveMessage", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ReceiveMessageResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def ResetMsgSubOffsetByTimestamp(self, request):
        """根据时间戳进行消息回溯，精确到毫秒

        :param request: Request instance for ResetMsgSubOffsetByTimestamp.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.ResetMsgSubOffsetByTimestampRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.ResetMsgSubOffsetByTimestampResponse`

        """
        try:
            params = request._serialize()
            body = self.call("ResetMsgSubOffsetByTimestamp", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.ResetMsgSubOffsetByTimestampResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def RewindCmqQueue(self, request):
        """回溯cmq队列

        :param request: Request instance for RewindCmqQueue.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.RewindCmqQueueRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.RewindCmqQueueResponse`

        """
        try:
            params = request._serialize()
            body = self.call("RewindCmqQueue", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.RewindCmqQueueResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SendBatchMessages(self, request):
        """批量发送消息

        注意：TDMQ 批量发送消息的接口是在 TDMQ-HTTP 的服务侧将消息打包为一个 Batch，然后将该 Batch 在服务内部当作一次 TCP 请求发送出去。所以在使用过程中，用户还是按照单条消息发送的逻辑，每一条消息是一个独立的 HTTP 的请求，在 TDMQ-HTTP 的服务内部，会将多个 HTTP 的请求聚合为一个 Batch 发送到服务端。即，批量发送消息在使用上与发送单条消息是一致的，batch 的聚合是在 TDMQ-HTTP 的服务内部完成的。

        :param request: Request instance for SendBatchMessages.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.SendBatchMessagesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.SendBatchMessagesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendBatchMessages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendBatchMessagesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SendCmqMsg(self, request):
        """发送cmq消息

        :param request: Request instance for SendCmqMsg.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.SendCmqMsgRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.SendCmqMsgResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendCmqMsg", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendCmqMsgResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SendMessages(self, request):
        """发送单条消息

        :param request: Request instance for SendMessages.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.SendMessagesRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.SendMessagesResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendMessages", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendMessagesResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def SendMsg(self, request):
        """此接口仅用于测试发生消息，不能作为现网正式生产使用

        :param request: Request instance for SendMsg.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.SendMsgRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.SendMsgResponse`

        """
        try:
            params = request._serialize()
            body = self.call("SendMsg", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.SendMsgResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)


    def UnbindCmqDeadLetter(self, request):
        """解绑cmq死信队列

        :param request: Request instance for UnbindCmqDeadLetter.
        :type request: :class:`tencentcloud.tdmq.v20200217.models.UnbindCmqDeadLetterRequest`
        :rtype: :class:`tencentcloud.tdmq.v20200217.models.UnbindCmqDeadLetterResponse`

        """
        try:
            params = request._serialize()
            body = self.call("UnbindCmqDeadLetter", params)
            response = json.loads(body)
            if "Error" not in response["Response"]:
                model = models.UnbindCmqDeadLetterResponse()
                model._deserialize(response["Response"])
                return model
            else:
                code = response["Response"]["Error"]["Code"]
                message = response["Response"]["Error"]["Message"]
                reqid = response["Response"]["RequestId"]
                raise TencentCloudSDKException(code, message, reqid)
        except Exception as e:
            if isinstance(e, TencentCloudSDKException):
                raise
            else:
                raise TencentCloudSDKException(e.message, e.message)