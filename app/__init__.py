
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#from flask.ext.openid import OpenID
#from flask.ext.mail import Mail
#from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')
#db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
from app import views,models