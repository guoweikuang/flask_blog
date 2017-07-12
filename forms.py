# -*- coding: utf-8 -*-
import re

from flask_wtf import FlaskForm
from wtforms import StringField, TextField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length


def custom_email(form_object, field_object):
    """自定义检验器，邮箱格式检验"""
    if not re.match(r"[^@+@[^@]+\.[^@]]+", field_object):
        raise ValidationError(u'邮箱地址格式不对！！！')


class CommentForm(FlaskForm):
    """评论表单"""
    name = StringField(u'名字', validators=[DataRequired(), Length(max=255)])
    text = TextField(u"内容", validators=[DataRequired()])






