# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask import render_template, redirect, url_for
from main import app
import models
from models import db
from my_blog.controller import blog


manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('server', Server(host='localhost', port=8089))
manage.add_command('db', MigrateCommand)
db.init_app(app)


@manage.shell
def make_shell_context():
    return dict(app=app,
                db=db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag)


@app.route('/')
def index():
    return redirect(url_for('my_blog.home'))

app.register_blueprint(blog.blog_buleprint)


if __name__ == '__main__':
    app.run()
