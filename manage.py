# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flask import render_template
from main import app
import models



manage = Manager(app)
migrate = Migrate(app, models.db)
manage.add_command('server', Server(host='localhost', port=8089))
manage.add_command('db', MigrateCommand)


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
    return render_template('index.html')


if __name__ == '__main__':
    manage.run()
