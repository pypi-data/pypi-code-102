#!/usr/bin/python
# encoding: utf-8
import requests
import json
import base64
import hashlib


class Idphoto:
    def __init__(self, appcode, timeout=7):
        self.appcode = appcode
        self.timeout = timeout
        self.make_idphoto_url = 'https://alidphoto.aisegment.com/idphoto/make'
        self.idphoto_arrange_url = 'https://idphotox.market.alicloudapi.com/idphoto/arrange'
        self.change_of_bg_url = 'https://idphotobg.market.alicloudapi.com/changebg'
        self.idphoto_detect_url = 'https://idpdetect.market.alicloudapi.com/idphoto/detect'
        self.env_detect_url = 'https://idphotov.market.alicloudapi.com/idphoto/env_detect'
        self.headrgba_url = 'https://person.market.alicloudapi.com/segment/person/headrgba'
        self.header_alpha_url = "https://person.market.alicloudapi.com/segment/person/head"
        self.face_alpha_url = "https://person.market.alicloudapi.com/segment/person/face"
        self.headborder_url = "https://person.market.alicloudapi.com/segment/person/headborder"
        self.person_hair_url = "https://person.market.alicloudapi.com/segment/person/hair"
        self.matting_url = "https://aliapi.aisegment.com/segment/matting"
        self.mattingborder_url = "https://aliapi.aisegment.com/segment/mattingborder"
        self.person_alpha_url = "https://aliapi.aisegment.com/segment/alpha"
        self.commonseg_rgba_url = "https://objseg.market.alicloudapi.com/commonseg/rgba"
        self.idphoto_preview_url = "https://idphotohq-open.segapi.com/preview"
        self.idphoto_take_url = "https://idphotohq-open.segapi.com/take"

        self.repair_image_url = 'https://repair.market.alicloudapi.com/repair/image'  # 智能修复

        self.headers = {
            'Authorization': 'APPCODE ' + appcode,
        }

    def get_md5_data(self, body):
        """
        md5加密
        :param body_json:
        :return:
        """

        md5lib = hashlib.md5()
        md5lib.update(body.encode("utf-8"))
        body_md5 = md5lib.digest()
        body_md5 = base64.b64encode(body_md5)
        return body_md5

    def get_photo_base64(self, file_path):
        with open(file_path, 'rb') as fp:
            photo_base64 = base64.b64encode(fp.read())

        photo_base64 = photo_base64.decode('utf8')
        return photo_base64

    def aiseg_request(self, url, data, headers):
        resp = requests.post(url=url, data=data, headers=headers, timeout=self.timeout)
        res = {"status_code": resp.status_code}
        try:
            res["data"] = json.loads(resp.text)
            return res
        except Exception as e:
            res["data"] = e
            return res

    def make_idphoto(self, file_path, bk, spec="5"):
        """
        证件照制作接口
        :param file_path:
        :param bk:
        :param spec:
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)

        body_json = {
            "photo": photo_base64,
            "bk": bk,
            "with_photo_key": 1,
            "spec": spec,
            "type": "jpg"
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.make_idphoto_url, data=body, headers=self.headers)
        return data

    def idphoto_arrange(self, photo_key, paper="inch6"):
        """
        证件照排版接口
        :param photo_key:
        :param paper:
        :return:
        """

        data = {"paper": paper, "photo_key": photo_key}
        headers = {"Authorization": self.headers["Authorization"]}
        data = self.aiseg_request(url=self.idphoto_arrange_url, data=data, headers=headers)
        return data

    def change_of_bg(self, photo_key, bk):
        """
        证据照更换背景
        :param photo_key:
        :param bk:
        :return:
        """
        body_json = {"photo_key": photo_key, "bk": bk}

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.change_of_bg_url, data=body, headers=self.headers)
        return data

    def idphoto_detect(self, photo, photo_key):
        """
        证件照成品检测接口
        photo和photo_key设置一个即可，如果两个都设置，则使用photo参数
        :param photo:
        :param photo_key:
        :return:
        """
        body_json = {
            "photo": photo,
            "photo_key": photo_key
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.idphoto_detect_url, data=body, headers=self.headers)
        return data

    def env_idphoto_detect(self, file_path, spec=None, with_photo_key=0):
        """
        证件照环境检测接口
        :param file_path:
        :param spec:
        :param with_photo_key:
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)

        body_json = {
            "photo": photo_base64,
            "spec": spec,
            "with_photo_key": with_photo_key
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.env_detect_url, data=body, headers=self.headers)
        return data

    def headrgba(self, file_path, type="jpg", is_crop_content=0):
        """
        人体头部抠图返回透明背景
        :param file_path:
        :param type:
        :param is_crop_content:
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)

        body_json = {
            "photo": photo_base64,
            "type": type,
            "is_crop_content": is_crop_content
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.headrgba_url, data=body, headers=self.headers)
        return data

    def header_alpha(self, file_path, type="jpg"):
        """
        人体头部抠图返回alpha通道
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "photo": photo_base64,
            "type": type
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.header_alpha_url, data=body, headers=self.headers)
        return data

    def face_alpha(self, file_path, type="jpg"):
        """
        人体脸部抠图接口_不含头发
        :return:
        """

        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "photo": photo_base64,
            "type": type
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.face_alpha_url, data=body, headers=self.headers)
        return data

    def head_border(self, file_path, type="jpg", border_ratio="0.1", margin_color="#ffffff"):
        """
        人体头部抠图带白边
        :return:
        """

        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "photo": photo_base64,
            "type": type,
            "border_ratio": border_ratio,
            "margin_color": margin_color
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.headborder_url, data=body, headers=self.headers)
        return data

    def person_hair(self, file_path, type="jpg"):
        """
        人体头发抠图
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "photo": photo_base64,
            "type": type
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.person_hair_url, data=body, headers=self.headers)
        return data

    def matting(self, file_path, type="jpg", face_required=0, is_crop_content=0):
        """
        人像抠图返回透明背景
        :param file_path:
        :param type:
        :param face_required:
        :param is_crop_content:
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "type": type,
            "photo": photo_base64,
            "face_required": face_required,
            "is_crop_content": is_crop_content
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.matting_url, data=body, headers=self.headers)
        return data

    def matting_border(self, file_path, type="jpg", margin_color="#ffffff", border_ratio=0, face_required=0):
        """
        人像抠图返回加边图
        :param file_path:
        :param type:
        :param face_required:
        :param is_crop_content:
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "type": type,
            "photo": photo_base64,
            "margin_color": margin_color,
            "border_ratio": border_ratio,
            "face_required": face_required
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.mattingborder_url, data=body, headers=self.headers)
        return data

    def person_alpha(self, file_path, type="jpg", face_required=0):
        """
        人像抠图返回alpha通道
        :return:
        """

        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "type": type,
            "photo": photo_base64,
            "face_required": face_required
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)

        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.person_alpha_url, data=body, headers=self.headers)
        return data

    def commonseg_rgba(self, file_path):
        """
        普通物体抠图_返回透明背景
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "photo": photo_base64,
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)

        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.commonseg_rgba_url, data=body, headers=self.headers)
        return data

    def idphoto_preview(self, file_path, spec=5, bk_list=["white", "red", "#887799"], beauty_degree=1,
                        photo_key=None):
        """
        证件照高惊版预览
        :param file_path:
        :return:
        """
        photo_base64 = self.get_photo_base64(file_path)
        body_json = {
            "photo": photo_base64,
            "spec": spec,
            "bk_list": bk_list,
            "beauty_degree": beauty_degree,
            "photo_key": photo_key
        }

        body = json.dumps(body_json)
        body_md5 = self.get_md5_data(body=body)

        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.idphoto_preview_url, data=body, headers=self.headers)
        return data

    def idphoto_take(self, photo_key, paper="inch6"):
        """
        证件照高精细下载
        :return:
        """
        data = {"paper": paper, "photo_key": photo_key}

        body = json.dumps(data)
        body_md5 = self.get_md5_data(body=body)

        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.idphoto_take_url, data=body, headers=self.headers)
        return data

    def repair_image(self, file_path, mask_path):
        """
        证件照智能修复
        :return:
        """
        img_photo_base64 = self.get_photo_base64(file_path)
        mask_photo_base64 = self.get_photo_base64(mask_path)

        data = {
            'mask': mask_photo_base64,
            'image': img_photo_base64
        }
        body = json.dumps(data)
        body_md5 = self.get_md5_data(body=body)
        self.headers.update({'Content-MD5': body_md5})

        data = self.aiseg_request(url=self.repair_image_url, data=body, headers=self.headers)
        return data

