# -*- coding: utf-8 -*-
"""
配置文件
"""


class Config(object):
    """基础配置，其他配置均从该类继承"""
    SECRET_KEY = "GUO_wei_@@_kuang__hello__world"
    RECAPTCHA_PUBLIC_KEY = "6LfrrSgUAAAAAJG2S1M180ZSW6uwh9Uz_NWZmq7I"
    RECAPTCHA_PRIVATE_KEY = "6LfrrSgUAAAAAA8CpJzIVc7c_YXvUox6Ev-PEO_M"


class DevConfig(Config):
    """开发模式配置"""
    DEDUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:2014081029@localhost:3306/flask_blog'


class TestConfig(Config):
    """测试模式配置"""
    pass


class DebugConfig(Config):
    """调试模式配置"""
    pass
