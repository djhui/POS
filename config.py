from flask import Flask
import MySQLdb
from flask.ext.sqlalchemy import SQLAlchemy
SECRET_KEY  = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
SQLALCHEMY_DATABASE_URI =  'mysql://root:123456@127.0.0.1/flask'
SQLALCHEMY_TRACK_MODIFICATIONS = True