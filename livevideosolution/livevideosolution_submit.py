#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
易盾反垃圾云服务直播音视频解决方案检测提交接口python示例代码
接口文档: http://dun.163.com/api.html
python版本：python3.7
运行:
    1. 修改 SECRET_ID,SECRET_KEY 为对应申请到的值
    2. $ python livevideosolution_submit.py
"""
__author__ = 'yidun-dev'
__date__ = '2019/11/27'
__version__ = '0.2-dev'

import hashlib
import time
import random
import urllib.request as urlrequest
import urllib.parse as urlparse
import json
from gmssl import sm3, func


class LiveVideoSolutionSubmitAPIDemo(object):
    """直播音视频解决方案检测提交接口示例代码"""

    API_URL = "http://as.dun.163.com/v2/livewallsolution/submit"
    VERSION = "v2.1"  # 直播音视频解决方案版本v2.1及以上语音二级细分类结构进行调整

    def __init__(self, secret_id, secret_key):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
        """
        self.secret_id = secret_id
        self.secret_key = secret_key

    def gen_signature(self, params=None):
        """生成签名信息
        Args:
            params (object) 请求参数
        Returns:
            参数签名md5值
        """
        buff = ""
        for k in sorted(params.keys()):
            buff += str(k) + str(params[k])
        buff += self.secret_key
        if "signatureMethod" in params.keys() and params["signatureMethod"] == "SM3":
            return sm3.sm3_hash(func.bytes_to_list(bytes(buff, encoding='utf8')))
        else:
            return hashlib.md5(buff.encode("utf8")).hexdigest()

    def check(self, params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        # params["signatureMethod"] = "SM3"  # 签名方法，默认MD5，支持SM3
        params["signature"] = self.gen_signature(params)

        try:
            params = urlparse.urlencode(params).encode("utf8")
            request = urlrequest.Request(self.API_URL, params)
            content = urlrequest.urlopen(request, timeout=1).read()
            return json.loads(content)
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    SECRET_ID = "your_secret_id"  # 产品密钥ID，产品标识
    SECRET_KEY = "your_secret_key"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
    api = LiveVideoSolutionSubmitAPIDemo(SECRET_ID, SECRET_KEY)

    # 私有请求参数
    params = {
        "url": "http://xxx.xx",
        "dataId": "fbfcad1c-dba1-490c-b4de-e784c2691765",
        # "callback": "{\"p\":\"xx\"}"
        # "scFrequency": "5"
    }

    ret = api.check(params)
    if ret is not None:
        code: int = ret["code"]
        msg: str = ret["msg"]
        if code == 200:
            result: dict = ret["result"]
            taskId: str = result["taskId"]
            status: bool = result["status"]
            if status:
                print("SUBMIT SUCCESS: taskId=%s" % taskId)
            else:
                print("SUBMIT FAIL: taskId=%s" % taskId)
        else:
            print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))
