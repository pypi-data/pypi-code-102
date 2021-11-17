from src.enums import Directions, ThingOrders
import requests
import json


class Client:
    def __init__(self, gatewayAddress):
        self.gatewayAddress = gatewayAddress

    def token(self, email, password):
        r = self.__http_do(
            path="/api-gw/v1/user/login",
            method="post",
            token="",
            data={"email": email, "password": password}
        )

        response = r.json()

        if not response.get("token"):
            raise Exception("invalid response: " + json.dumps(response))

        parts = response.get("token").split(" ")
        if len(parts) != 2:
            raise Exception("invalid response: " + json.dumps(response))

        return parts[1]

    def token_verify(self, token):
        try:
            self.__http_do(
                path="/api-gw/v1/user/verify",
                method="get",
                token=token,
                data=None
            )
            return True
        except:
            return False

    def reset_password(self, token, new_pw, old_pw):
        self.__http_do(
            path="/api-gw/v1/user/reset-password",
            method="post",
            token=token,
            data={
                "newPassword": new_pw,
                "oldPassword": old_pw,
            }
        )

    def user_profile(self, token):
        response = self.__http_do(
            path="/api-gw/v1/user/profile",
            method="get",
            token=token,
            data=None
        )

        jsonBody = response.json()

        return {
            "id": jsonBody.get("id"),
            "email": jsonBody.get("email"),
            "fullname": jsonBody.get("fullName"),
            "phone_number": jsonBody.get("phoneNumber"),
            "customer_id": jsonBody.get("customerId"),
            "user_status_id": jsonBody.get("userStatusId"),
            "user_group_id": jsonBody.get("userGroupId"),
            "description": jsonBody.get("desc"),
            "created_by": jsonBody.get("createdBy")
        }

    def create_thing(self, token, name, metadata):
        self.__http_do(
            path="/api-gw/v1/thing",
            method="post",
            token=token,
            data={
                "name": name,
                "metadata": metadata,
            },
        )

    def list_things_by_user(self, token, offset=0, limit=10, direction=Directions.Asc, order=ThingOrders.ID):
        response = self.__http_do(
            path="/api-gw/v1/thing/list",
            method="get",
            token=token,
            data={
                "offset": offset,
                "limit": limit,
                "dir": direction,
                "order": order,
            }
        )

        return response.json()

    def delete_thing(self, token, thing_id):
        self.__http_do(
            path="/api-gw/v1/thing/"+thing_id,
            method="delete",
            token=token,
        )

    def thing_profile(self, token, thing_id):
        response = self.__http_do(
            path="/api-gw/v1/thing/"+thing_id,
            method="get",
            token=token,
        )

        body = response.json()

        return {
            "id": body.get("id"),
            "key": body.get("key"),
            "name": body.get("name"),
            "metadata": body.get("metadata")
        }

    def update_thing(self, token, thing_id, name, metadata=None):
        self.__http_do(
            path="/api-gw/v1/thing",
            method="put",
            token=token,
            data={
                "id": thing_id,
                "name": name,
                "metadata": metadata,
            }
        )

    def list_channels_by_thing(self, token, thing_id, offset=0, limit=10, order=Directions.Asc, direction=ThingOrders.ID, disconnected=False):
        response = self.__http_do(
            path='/api-gw/v1/thing/%s/channels' % thing_id,
            method="get",
            token=token,
            data={
                "offset": offset,
                "limit": limit,
                "order": order,
                "dir": direction,
                "disconnected": disconnected,
            },
        )

        return response.json()

    def connect(self, token, channel_ids, thing_ids):
        self.__http_do(
            path="/api-gw/v1/thing/connect",
            method="post",
            token=token,
            data={
                "channel_ids": channel_ids,
                "thing_ids": thing_ids,
            },
        )

    def disconnect(self, token, channel_id, thing_id):
        self.__http_do(
            path="/api-gw/v1/thing/%s/channel/%s" % (thing_id, channel_id),
            method="delete",
            token=token,
        )

    def create_channel(self, token, name, metadata=None):
        self.__http_do(
            path="/api-gw/v1/channel",
            method="post",
            token=token,
            data={
                "name": name,
                "metadata": metadata,
            },
        )

    def update_channel(self, token, thing_id, name, metadata=None):
        self.__http_do(
            path="/api-gw/v1/channel",
            method="put",
            token=token,
            data={
                "id": thing_id,
                "name": name,
                "metadata": metadata,
            },
        )

    def delete_channel(self, token, channel_id):
        self.__http_do(
            path="/api-gw/v1/channel/" + channel_id,
            method="delete",
            token=token,
        )

    def channel_profile(self, token, channel_id):
        response = self.__http_do(
            path="/api-gw/v1/channel/" + channel_id,
            method="get",
            token=token,
        )

        body = response.json()

        return {
            "id": body["id"],
            "name": body["name"],
            "metadata": body["metadata"]
        }

    def list_channels_by_user(self, token,  offset=0, limit=10, order=Directions.Asc, direction=ThingOrders.ID):
        response = self.__http_do(
            path="/api-gw/v1/channel/list",
            method="get",
            token=token,
            data={
                "offset": offset,
                "limit": limit,
                "order": order,
                "direction": direction
            }
        )
        return response.json()

    def create_gateway(self, token, thing_id, name, description=None):
        self.__http_do(
            path="/api-gw/v1/gateway/create",
            method="post",
            token=token,
            data={
                "name": name,
                "thingId": thing_id,
                "description": description
            }
        )

    def upate_gateway(self, token, gate_id, name, description):
        self.__http_do(
            path="/api-gw/v1/gateway/edit",
            method="put",
            token=token,
            data={
                "id": gate_id,
                "name": name,
                "description": description
            }
        )

    def delete_gateway(self, token, gate_id):
        self.__http_do(
            path="/api-gw/v1/gateway/" + gate_id,
            method="delete",
            token=token,
        )

    def gateway_profile(self, token, gate_id):
        response = self.__http_do(
            path="/api-gw/v1/gateway/" + gate_id,
            method="get",
            token=token,
        )

        body = response.json()

        return {
            "id": body["gatewayId"],
            "name": body["gatewayName"],
            "description": body["gatewayDes"],
            "owner": body["gatewayOwner"],
            "underlay_thing": {
                "id": body["thingId"],
                "name": body["thingName"],
                "key": body["thingKey"],
                "metadata": body["metadata"]
            }
        }

    def list_gateway(self, token):
        response = self.__http_do(
            path="/api-gw/v1/gateway/list",
            method="get",
            token=token,
        )

        ret = []

        for gateway in response.json():
            ret.append({
                "id": gateway["gatewayId"],
                "name": gateway["gatewayName"],
                "description": gateway["gatewayDes"],
                "owner": gateway["gatewayOwner"],
                "underlay_thing": {
                    "id": gateway["thingId"],
                    "name": gateway["thingName"],
                    "key": gateway["thingKey"],
                    "metadata": gateway["metadata"]
                }
            })

        return ret

    def gateway_status(self, token):
        response = self.__http_do(
            path="/api-gw/v1/gateway/status",
            method="get",
            token=token,
        )

        return response.json()

    def gateway_active_device_count(self, token, gate_id):
        response = self.__http_do(
            "/api-gw/v1/gateway/active-device-count/" + gate_id,
            method="get",
            token=token,
        )

        return response.json()

    def __http_do(self, path, method, token, data=None):
        headers = {}

        if token:
            headers["Authorization"] = "Bearer %s" % token

        r = requests.request(
            url=self.gatewayAddress + path,
            method=method,
            headers=headers,
            json=data,
        )

        if r.status_code != 200 and r.status_code != 201:
            raise Exception("aiot.client error: " + r.text)

        return r
