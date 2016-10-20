#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/flask'
db = SQLAlchemy(app)
 
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
    orderdate = db.Column(db.Date)
    wangwang = db.Column(db.String(120))
    cdeliverydate = db.Column(db.Date) #Cumstomer wants to delivery data
    type = db.Column(db.String(120))
    color = db.Column(db.String(120))
    number = db.Column(db.Integer)
    address = db.Column(db.VARCHAR(520))
    trancorp = db.Column(db.VARCHAR(520))
    transportation = db.Column(db.VARCHAR(520))
    Inprice = db.Column(db.Float) #Insurance price
    price = db.Column(db.Float) #sales price
    advprice = db.Column(db.Float) #Advance fee
    CSE = db.Column(db.String(120)) #Customer Service Employee
    deliverydate = db.Column(db.Date) #actual delivery date
    Tnumber = db.Column(db.String(120)) #transportation number
    Aprice = db.Column(db.Float) #Actual price
    Recashes = db.Column(db.Float) #Cash back
    Commission = db.Column(db.Date)
    memo = db.Column(db.VARCHAR(520))

  
    def __init__(self, picture="0", orderdate="0000-00-00", wangwang="0", cdeliverydate="0000-00-00", type="0",color="0",number=0,address="",transportation="-",Inprice=0,price=0,advprice=0,CSE=0,deliverydate="0000-00-00", trancorp="", Tnumber="", Aprice=0,Recashes=0,Commission=0,  memo="no comments"):
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
        self.price = price
        self.advprice = advprice
        self.CSE = CSE
        self.deliverydate = deliverydate
        self.trancorp = trancorp
        self.Tnumber = Tnumber
        self.Aprice = Aprice
        self.Recashes = Recashes
        self.Commission = Commission
        self.memo = memo


class Trans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corpname = db.Column(db.String(80), unique=True)
   
  
    def __init__(self, corpname):
        self.corpname = corpname

class Cates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ecate = db.Column(db.String(80), unique=True)
    categroies = db.Column(db.String(80), unique=True)

    def __init__(self, ecate,categroies):
        self.ecate=ecate
        self.categroies = categroies

class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery = db.Column(db.String(80), unique=True)

    def __init__(self, delivery):
        self.delivery = delivery

class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=db.func.CURRENT_TIMESTAMP())
    events = db.Column(db.VARCHAR(520))
    eventlevel = db.Column(db.String(80))

    def __init__(self, date, events):
        self.date  = date
        self.events  = events
        self.eventlevel  = eventlevel

class Freight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deliveryplace = db.Column(db.String(80), unique=True)
    destprovice = db.Column(db.String(80))
    destcity = db.Column(db.String(80))
    price = db.Column(db.Float)
    dropofffee = db.Column(db.Float)
    cheapest = db.Column(db.Float)
    transtype = db.Column(db.String(80))
    TBOST = db.Column(db.String(80))
    #发货地，目的省，目的市，每方价格，送货费，最低一票，快慢类型，自提时效

    def __init__(self, deliveryplace,destprovice,destcity,price,dropofffee,cheapest,transtype,TBOST):
        self.deliveryplace=deliveryplace
        self.destprovice = destprovice
        self.destcity = destcity
        self.price = price
        self.dropofffee = dropofffee
        self.cheapest = cheapest
        self.transtype = transtype
        self.TBOST = TBOST


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    #Create init account,username=admin password=admin encrypted by sha256
    insetuser=User(username='admin', password='c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec', role='admin',nickname='系统管理员',mobile="")
    #create init role
    insetrole=Role('admin',1,1,1,1,1,1,1,1,1,1,1,1)
    insettrans = Trans(u"新邦物流")
    insettrans1 = Trans(u"德邦物流")
    db.session.add(Cates("cabinets",u"柜/箱"))
    db.session.add(Cates("chairs",u"椅/凳"))
    db.session.add(Cates("desks",u"桌/几"))
    db.session.add(Cates("sofa",u"沙发"))
    db.session.add(Delivery(u"预付-自提"))
    db.session.add(Delivery(u"预付-送货到楼下"))
    db.session.add(Delivery(u"到付-自提"))
    db.session.add(Delivery(u"到付-送货到楼下"))
    db.session.add(insettrans)
    db.session.add(insettrans1)
    db.session.add(insetuser)
    db.session.add(insetrole)
    db.session.commit()