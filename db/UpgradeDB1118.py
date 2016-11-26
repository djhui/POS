#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/flask'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class Salesorder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productid0 = db.Column(db.String(120))
    warehouse0 = db.Column(db.String(120))
    code0 = db.Column(db.String(120))
    number0 = db.Column(db.Integer)
    productid1 = db.Column(db.String(120))
    warehouse1 = db.Column(db.String(120))
    code1 = db.Column(db.String(120))
    number1 = db.Column(db.Integer)
    productid2 = db.Column(db.String(120))
    warehouse2 = db.Column(db.String(120))
    code2 = db.Column(db.String(120))
    number2 = db.Column(db.Integer)
    productid3 = db.Column(db.String(120))
    warehouse3 = db.Column(db.String(120))
    code3 = db.Column(db.String(120))
    number3 = db.Column(db.Integer)
    productid4 = db.Column(db.String(120))
    warehouse4 = db.Column(db.String(120))
    code4 = db.Column(db.String(120))
    number4 = db.Column(db.Integer)
    productid5 = db.Column(db.String(120))
    warehouse5 = db.Column(db.String(120))
    code5 = db.Column(db.String(120))
    number5 = db.Column(db.Integer)
    productid6 = db.Column(db.String(120))
    warehouse6 = db.Column(db.String(120))
    code6 = db.Column(db.String(120))
    number6 = db.Column(db.Integer)
    productid7 = db.Column(db.String(120))
    warehouse7 = db.Column(db.String(120))
    code7 = db.Column(db.String(120))
    number7 = db.Column(db.Integer)
    productid8 = db.Column(db.String(120))
    warehouse8 = db.Column(db.String(120))
    code8 = db.Column(db.String(120))
    number8 = db.Column(db.Integer)
    productid9 = db.Column(db.String(120))
    warehouse9 = db.Column(db.String(120))
    code9 = db.Column(db.String(120))
    number9 = db.Column(db.Integer)
    remark = db.Column(db.String(120))
    offset = db.Column(db.Boolean(1))

    def __init__(self, productid0, warehouse0, code0, number0, productid1, warehouse1, code1, number1, productid2, warehouse2, code2, number2, productid3, warehouse3, code3, number3, productid4, warehouse4, code4, number4, productid5, warehouse5, code5, number5, productid6, warehouse6, code6, number6, productid7, warehouse7, code7, number7, productid8, warehouse8, code8, number8, productid9, warehouse9, code9, number9, remark, offset):
        self.productid0 = productid0
        self.warehouse0 = warehouse0
        self.code0 = code0
        self.number0 = number0
        self.productid1 = productid1
        self.warehouse1 = warehouse1
        self.code1 = code1
        self.number1 = number1
        self.productid2 = productid2
        self.warehouse2 = warehouse2
        self.code2 = code2
        self.number2 = number2
        self.productid3 = productid3
        self.warehouse3 = warehouse3
        self.code3 = code3
        self.number3 = number3
        self.productid4 = productid4
        self.warehouse4 = warehouse4
        self.code4 = code4
        self.number4 = number4
        self.productid5 = productid5
        self.warehouse5 = warehouse5
        self.code5 = code5
        self.number5 = number5
        self.productid6 = productid6
        self.warehouse6 = warehouse6
        self.code6 = code6
        self.number6 = number6
        self.productid7 = productid7
        self.warehouse7 = warehouse7
        self.code7 = code7
        self.number7 = number7
        self.productid8 = productid8
        self.warehouse8 = warehouse8
        self.code8 = code8
        self.number8 = number8
        self.productid9 = productid9
        self.warehouse9 = warehouse9
        self.code9 = code9
        self.number9 = number9
        self.remark = remark
        self.offset = offset
def upgrade():
    db.create_all()

def downgrade():
    db.drop_all()

if __name__ == '__main__':
    downgrade()
    upgrade()