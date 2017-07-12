# -*- coding: utf-8 -*-
import os

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
# from flask import render_template, redirect, url_for, Flask
# from main import app
# from config import DevConfig
# import models
# from models import db
# from my_blog.controller import blog
from my_blog import create_app
from my_blog import models


#app = Flask(__name__)
#app.config.from_object(DevConfig)
env = os.environ.get('BLOG_ENV', 'dev')
app = create_app('my_blog.config.%sConfig' % env.capitalize())
manage = Manager(app)
migrate = Migrate(app, models.db)
manage.add_command('server', Server(host='localhost', port=8089))
manage.add_command('db', MigrateCommand)
# db.init_app(app)


@manage.shell
def make_shell_context():
    return dict(app=app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag,
                Server=Server)


#@app.route('/')
#def index():
#    return redirect(url_for('my_blog.home'))
#

if __name__ == '__main__':
    manage.run()
