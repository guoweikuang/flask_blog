# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from main import app
import models


manage = Manager(app)
manage.add_command('server', Server())


@manage.shell
def make_shell_context():
    return dict(app=app,
                db=models.db,
                User=models.User,
                Post=models.Post,
                Comment=models.Comment,
                Tag=models.Tag)


@app.route('/')
def index():
    return '<h1>hello, world!</h1>'


if __name__ == '__main__':
    manage.run()
