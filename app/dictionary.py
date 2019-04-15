# -*- coding: utf-8 -*-

"""
字典翻译

字典翻译使用有道智云文本翻译
@link: https://ai.youdao.com/docs/doc-trans-api.s
"""

import time
import uuid
import hashlib
from app.packages.workflow import web
from app.config import APPKEY, APPSECRET


class Dictionary(object):
    __URL = 'http://openapi.youdao.com/api'

    def input(self, query):
        return query if 20 >= len(query) else '{prefix}{length}{postfix}'.format(prefix=query[0:10], length=len(query), postfix=query[-10:])

    def translate(self, query):
        salt = str(uuid.uuid1())
        curtime = str(int(time.time()))
        sign_hash = hashlib.sha256()
        sign_hash.update('{appKey}{input}{salt}{curtime}{appSecret}'.format(
            appKey=APPKEY,
            input=self.input(query),
            salt=salt,
            curtime=curtime,
            appSecret=APPSECRET
        ).encode('utf-8'))
        sign = sign_hash.hexdigest()
        params = {
            'q': query,
            'from': 'auto',
            'to': 'auto',
            'appKey': APPKEY,
            'salt': salt,
            'sign': sign,
            'signType': 'v3',
            'curtime': curtime
        }
        response = web.get(url=self.__URL, params=params)
        response.raise_for_status()
        return response.json()


