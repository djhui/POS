#!/usr/bin/python
# -*- coding:utf-8 -*-
from hashlib import md5
from app import app
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    nickname = db.Column(db.String(80))
    mobile = db.Column(db.String(80))
    password = db.Column(db.String(320))
    role = db.Column(db.String(32))
  
    def __init__(self, username, password, role, mobile, nickname):
        self.username = username
        self.password = password
        self.role= role
        self.mobile = mobile
        self.nickname = nickname

    @staticmethod
    def make_unique_nickname(username):
        pass
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

        
    def __repr__(self):
        return '<User %r>' % (self.username)    
        


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(80), unique=True)
    sales = db.Column(db.Boolean(1))
    salesdetail = db.Column(db.Boolean(1))
    salesadd = db.Column(db.Boolean(1))
    freight = db.Column(db.Boolean(1))
    stock = db.Column(db.Boolean(1))
    stockcabinets = db.Column(db.Boolean(1))
    stockchairs = db.Column(db.Boolean(1))
    stockdesks = db.Column(db.Boolean(1))
    stocksofa = db.Column(db.Boolean(1))
    stockadd = db.Column(db.Boolean(1))
    account = db.Column(db.Boolean(1))
    role = db.Column(db.Boolean(1))
  
    def __init__(self, rolename=0, sales=0, salesdetail=0,salesadd=0,freight=0,stock=0,stockcabinets=0,stockchairs=0,stockdesks=0,stocksofa=0,stockadd=0,account=0,role=0):
        self.rolename = rolename
        self.sales = sales
        self.salesdetail= salesdetail
        self.salesadd = salesadd
        self.freight = freight
        self.stock = stock
        self.stockcabinets = stockcabinets
        self.stockchairs = stockchairs
        self.stockdesks = stockdesks
        self.stockdesks = stockdesks
        self.stocksofa = stocksofa
        self.stockadd = stockadd
        self.account = account
        self.role = role

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.VARCHAR(520), unique=True)
    products = db.Column(db.String(120))
    categroies = db.Column(db.String(120))
    code = db.Column(db.String(120))
    specification = db.Column(db.String(120))
    color = db.Column(db.String(120))
    exstock = db.Column(db.Integer)
    whstock = db.Column(db.Integer)
    fastock = db.Column(db.Integer)
    pkgsize = db.Column(db.String(120))
    pgkbulk = db.Column(db.String(120))
    memo = db.Column(db.VARCHAR(520))
  
    def __init__(self, picture="0", products="0", categroies="0", code="0", specification="0",color="0",exstock=0,whstock=0,fastock=0,pkgsize="0*0*0",pgkbulk="0*0*0",memo="no comments"):
        self.picture = picture
        self.products = products
        self.categroies = categroies
        self.code = code
        self.specification = specification
        self.color = color
        self.exstock = exstock
        self.whstock = whstock
        self.fastock = fastock
        self.pkgsize = pkgsize
        self.pgkbulk = pgkbulk
        self.memo = memo

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.VARCHAR(520), unique=True)
    orderdate = db.Column(db.DateTime)
    wangwang = db.Column(db.String(120))
    cdeliverydate = db.Column(db.DateTime) #Cumstomer wants to delivery data
    type = db.Column(db.String(120))
    color = db.Column(db.String(120))
    number = db.Column(db.Integer)
    address = db.Column(db.VARCHAR(520))
    transportation = db.Column(db.VARCHAR(520))
    Inprice = db.Column(db.Float) #Insurance price
    advprice = db.Column(db.Float) #Advance fee
    CSE = db.Column(db.String(120)) #Customer Service Employee
    deliverydate = db.Column(db.DateTime) #actual delivery date
    Tnumber = db.Column(db.String(120)) #transportation number
    Aprice = db.Column(db.Float) #Actual price
    Recashes = db.Column(db.Float) #Cash back
    Commission = db.Column(db.Float)
    memo = db.Column(db.VARCHAR(520))

  
    def __init__(self, picture="0", orderdate="0000-00-00", wangwang="0", cdeliverydate="0000-00-00", type="0",color="0",number=0,address="",transportation="-",Inprice=0,advprice=0,ces=0,deliverydate="0000-00-00", Tnumber="", Aprice=0,Recashes=0,Commission=0,  memo="no comments"):
        self.picture = picture
        self.orderdate = orderdate
        self.wangwang = wangwang
        self.cdeliverydate = cdeliverydate
        self.type = type
        self.color = color
        self.number = number
        self.address = address
        self.transportation = transportation
        self.Inprice = Inprice
        self.advprice = advprice
        self.CES = CES
        self.deliverydate = deliverydate
        self.Tnumber = Tnumber
        self.Aprice = Aprice
        self.Recashes = Recashes
        self.sCommission = Commission
        self.memo = memo
        
