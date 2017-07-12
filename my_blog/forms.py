# -*- coding: utf-8 -*-
import re

from flask_wtf import FlaskForm, RecaptchaField, Form

from wtforms.validators import DataRequired, Length, EqualTo, URL
from my_blog.models import User
from wtforms import (
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    ValidationError
)


def custom_email(form_object, field_object):
    """自定义检验器，邮箱格式检验"""
    if not re.match(r"[^@+@[^@]+\.[^@]]+", field_object):
        raise ValidationError(u'邮箱地址格式不对！！！')


class CommentForm(FlaskForm):
    """评论表单"""
    name = StringField(u'名字', [DataRequired(), Length(max=255)])
    text = TextField(u"内容", [DataRequired()])


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField(u"用户名", [DataRequired(), Length(max=255)])
    password = PasswordField(u"密码", [DataRequired()])
    remember_me = BooleanField(u"记住我")

    def validate(self):
        """核对用户信息"""
        check_validata = super(LoginForm, self).validate()

        if not check_validata:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append(u"无效的用户名或密码！")
            return False
        if not user.check_password(self.password.data):
            self.username.errors.append(u"无效的密码！")
            return False
        return True


class RegisterForm(FlaskForm):
    """注册模块"""
    username = StringField(u"用户名", [DataRequired(), Length(max=255)])
    password = PasswordField(u"密码", [DataRequired(), Length(min=8)])
    password_confirm = PasswordField(u"确认密码", [
                                            DataRequired(), EqualTo('password')])
    # recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        print(u'check', check_validate)
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append(u"用户已经存在！")
            return False
        return True


class PostForm(FlaskForm):
    """文章模块"""
    title = StringField(u"标题", [DataRequired(), Length(max=255)])
    text = TextAreaField(u"内容", [DataRequired()])



