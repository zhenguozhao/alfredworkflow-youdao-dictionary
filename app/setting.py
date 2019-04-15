# -*- coding: utf-8 -*-

"""
项目设置
"""

import logging

LOGGING_LEVEL = logging.CRITICAL
LOGGING_SETTING = dict(format="%(levelname)s\t%(message)s %(pathname)s(%(lineno)s)", level=LOGGING_LEVEL, filename='/tmp/log')
