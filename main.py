# -*- coding: utf-8 -*-
from flask import Flask
from config import DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)
