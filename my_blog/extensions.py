# -*- coding: utf-8 -*-
"""
扩展模块
"""
from flask_bcrypt import Bcrypt
from flask_oauth import OAuth
from flask_login import LoginManager
from flask import session


bcrypt = Bcrypt()
oauth = OAuth()
login_manager = LoginManager()


login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = u"请通过该页面登录"
login_manager.login_message_category = 'info'

facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key='1967955396784201',
    consumer_secret='3a09040a8a33e5e91036184a158fa5bd',
    request_token_params={'scope': 'email'}
)


@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_oauth_token')


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.filter_by(id=user_id).first()
