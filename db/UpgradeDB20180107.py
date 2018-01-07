#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@192.168.1.254/Alpha'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class FileUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120))
    uploadtime = db.Column(db.TIMESTAMP,server_default=func.now())
    

    def __init__(self, filename, uploadtime):
        self.filename = filename
        self.uploadtime = uploadtime
        
def upgrade():
    db.create_all()

def downgrade():
    db.drop_all()

if __name__ == '__main__':
    downgrade()
    upgrade()