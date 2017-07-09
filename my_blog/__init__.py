# -*- coding: utf-8 -*-
from flask import Flask
from config import DevConfig
import forms

app = Flask(__name__)
views = __import__('views')
app.config.from_object(DevConfig)
from views import blog_buleprint

if __name__ == '__main__':
    app.register_blueprint(blog_buleprint)
    app.run()

