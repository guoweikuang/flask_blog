# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for
from my_blog.models import db
from my_blog.controller import blog, main 
from my_blog.extensions import bcrypt
from flask_recaptcha import ReCaptcha


def create_app(object_name):
    """工厂函数"""
    app = Flask(__name__)
    app.config.from_object(object_name)
    recaptcha = ReCaptcha(app=app)

    db.init_app(app)
    bcrypt.init_app(app)
    recaptcha.init_app(app)

    @app.route('/')
    def index():
        return redirect(url_for('my_blog.home'))

    app.register_blueprint(blog.blog_buleprint)
    app.register_blueprint(main.main_blueprint)

    return app


# app = Flask(__name__)
# views = __import__('views')
# app.config.from_object(DevConfig)
# from views import blog_buleprint

# if __name__ == '__main__':
#     app.register_blueprint(blog_buleprint)
#     app.run()

