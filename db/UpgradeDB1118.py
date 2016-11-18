#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/flask'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class Sale_Pro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.String(120))
    warehouse = db.Column(db.String(120))
    number = db.Column(db.Integer)
    offset = db.Column(db.Boolean(1))

    def __init__(self, productid,warehouse, number,offset):
        self.productid = productid
        self.warehouse = warehouse
        self.number = number
        self.offset = offset
def upgrade():
    db.create_all()

def downgrade():
    db.drop_all()

if __name__ == '__main__':
    upgrade()