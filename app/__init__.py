#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler

#from flask.ext.openid import OpenID
#from flask.ext.mail import Mail
#from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


file_handler = RotatingFileHandler('/var/log/YFapp.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)
app.logger.info('App started')



from app import views,models