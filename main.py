# -*- coding: utf-8 -*-

import sys
import os
import logging
import hashlib
from app.setting import LOGGING_SETTING, LOGGING_LEVEL
from app.packages.workflow import Workflow3
from app.dictionary import Dictionary
from app.config import APPKEY, APPSECRET
from app.packages.workflow.notify import notify

# 指定编码解码方式
reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(**LOGGING_SETTING)


def encrypt(data):
    data_hash = hashlib.md5()
    data_hash.update(data)
    return data_hash.hexdigest()


def open_editor(file_path):
    os.system('open -e "{file}"'.format(file=file_path))


def main(workflow):
    # 检查存储配置信息
    if not all((APPKEY, APPSECRET)):
        notify('⚠️ 警告', '请先设置好相关配置信息！')
        open_editor('app/config.py')
        return

    args = workflow.args
    if 0 < len(args):
        query = ' '.join(args)
        dict_web_url = 'http://dict.youdao.com/w/{query}/'.format(query=query)
        store_key = '{name}.store'.format(name=encrypt(query))
        translate_data = workflow.stored_data(store_key)
        if translate_data is None:
            translate_data = Dictionary().translate(query)
            workflow.store_data(store_key, translate_data)

        if translate_data.has_key('basic') and translate_data['basic'] is not None:
            # 释义
            if str(translate_data['l']).endswith('2en'):
                workflow.add_item(title=' '.join(translate_data['translation']), subtitle='"⌘+C"键复制', copytext=' '.join(translate_data['translation']), valid=True, arg=dict_web_url)
            else:
                workflow.add_item(title=' '.join(translate_data['translation']), valid=True, arg=dict_web_url)

            # 基本释义
            if translate_data['basic'].has_key('explains') and translate_data['basic']['explains'] is not None:
                for item in translate_data['basic']['explains']:
                    if item != ' '.join(translate_data['translation']):
                        if str(translate_data['l']).endswith('2en'):
                            workflow.add_item(title=item, subtitle='"⌘+C"键复制', copytext=item, valid=True, arg=dict_web_url)
                        else:
                            workflow.add_item(title=item, valid=True, arg=dict_web_url)
        else:
            # 释义
            workflow.add_item(title=' '.join(translate_data['translation']), valid=True, arg=dict_web_url)

    workflow.send_feedback()


if __name__ == '__main__':
    workflow = Workflow3()
    workflow.logger.setLevel(LOGGING_LEVEL)
    sys.exit(workflow.run(main))
