# -*- coding: utf-8 -*-
"""
配置文件
"""


class Config(object):
    """基础配置，其他配置均从该类继承"""
    SECRET_KEY = "GUO_wei_@@_kuang__hello__world"


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
