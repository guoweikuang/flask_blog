# -*- coding: utf-8 -*-
import os
import logging
from uuid import uuid4

from flask import flash, redirect, url_for, render_template, Blueprint, request
from my_blog.forms import LoginForm, RegisterForm
from my_blog.models import db, User
from my_blog.extensions import facebook
from flask_login impport login_user


main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=os.path.join(os.path.pardir, 'templates', 'main'),
    url_prefix='/main'
)


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
             flash(u"你已经登录了", category='success')
            return redirect(request.args.get('next') or url_for('my_blog.home'))
        # flash(u"你已经登录了", category='success')
        # return redirect(url_for('my_blog.home'))
    return render_template('login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    flash(u"你已经登出", category="success")
    return redirect(url_for('blog.home'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """View function for Register."""

    # Will be check the username whether exist.
    form = RegisterForm()
    print('hello, world')
    print(u'onclick', form.validate_on_submit())
    if form.validate_on_submit():
        new_user = User(id=str(uuid4()),
                        username=form.username.data,
                        password=form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Your user has been created, please login.',
              category="success")

        return redirect(url_for('main.login'))
    return render_template('register.html',
                           form=form)


@main_blueprint.route('/facebook')
def facebook_login():
    return facebook.authorize(
        callback=url_for('main.facebook_authorized',
                         next=request.referrer or None,
                         external=True))


@main_blueprint.route('/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return u"请求已经拒绝：原因是%s, error: %s" % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['facebook_oauth_token'] = (resp['access_token'], '')
    
    me = facebook.get('/me')
    if me.data.get('first_name', False):
        facebook_username = me.data['first_name'] + " " + me.data['last_name']
    else:
        facebook_username = me.data['name']

    user = User.query.filter_by(username=facebook_username).first()
    if user is None:
        user = User(id=str(uuid4()), username=facebook_username, password='gwk2014081029')
        db.session.add(user)
        db.session.commit()

    flash(u"你已经登录了！！", category="success")
    return redirect(url_for('my_blog.home'))

