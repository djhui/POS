#!/usr/bin/python
# -*- coding:utf-8 -*-
from hashlib import sha512
from datetime import datetime
SECRET_KEY = sha512(str(datetime.now())).hexdigest()
#SECRET_KEY = "fff"
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.1.254/flask'
SQLALCHEMY_TRACK_MODIFICATIONS = True
