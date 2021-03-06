#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/flask'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
class User(db.Model): #帐号表
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True) #用户名
    nickname = db.Column(db.String(80)) #别名
    mobile = db.Column(db.String(80)) #手机
    password = db.Column(db.String(320)) #密码
    role = db.Column(db.String(32),) #角色
  
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
    productid = db.Column(db.Integer)
    picture = db.Column(db.String(120))
    products = db.Column(db.String(120))
    code = db.Column(db.String(120))
    specification = db.Column(db.String(120))
    color = db.Column(db.String(120))
    exstock = db.Column(db.Integer)
    whstock = db.Column(db.Integer)
    fastock = db.Column(db.Integer)
    offset = db.Column(db.Boolean(1))
    memo = db.Column(db.VARCHAR(520))
  
    def __init__(self, productid="0",picture="", products="0",code="",specification="",color="", exstock=0,whstock=0,fastock=0,offset=0,memo="no comments"):
        self.productid = productid
        self.picture = picture
        self.products = products
        self.code = code
        self.specification = specification
        self.color = color
        self.exstock = exstock
        self.whstock = whstock
        self.fastock = fastock
        self.offset = offset
        self.memo = memo

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.VARCHAR(520))
    products = db.Column(db.String(120))
    categroies = db.Column(db.String(120))
    code = db.Column(db.String(120), unique=True)
    specification = db.Column(db.String(120))
    color = db.Column(db.String(120))
    exstock = db.Column(db.Integer)
    whstock = db.Column(db.Integer)
    fastock = db.Column(db.Integer)
    pkgsize = db.Column(db.String(120))
    pkgbulk = db.Column(db.Float)
    memo = db.Column(db.VARCHAR(520))
  
    def __init__(self, picture="0", products="0", categroies="0", code="0", specification="0",color="",exstock=0,whstock=0,fastock=0 , pkgsize="0*0*0",pkgbulk="6",memo="no comments"):
        self.picture = picture
        self.products = products
        self.categroies = categroies
        self.code = code
        self.specification = specification
        self.color = color
        self.exstock=exstock
        self.whstock=whstock
        self.fastock=fastock
        self.pkgsize = pkgsize
        self.pkgbulk = pkgbulk
        self.memo = memo

class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #productid = db.Column(db.Integer)
    picture = db.Column(db.String(500))
    orderdate = db.Column(db.Date)
    wangwang = db.Column(db.String(120))
    cdeliverydate = db.Column(db.Date) #Cumstomer wants to delivery data
    type1 = db.Column(db.String(120))
    color0 = db.Column(db.String(120))
    #number = db.Column(db.Integer)
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
    offset = db.Column(db.Boolean(1))
    memo = db.Column(db.VARCHAR(520))
    #warehouse = db.Column(db.String(120))

    productid0 = db.Column(db.Integer)
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
  
    def __init__(self, picture="",orderdate="0000-00-00", wangwang="0", cdeliverydate="0000-00-00", type1="0",address="",transportation="-",Inprice=0,price=0,advprice=0,CSE=0,deliverydate="0000-00-00", trancorp="", Tnumber="", Aprice=0,Recashes=0,Commission=0,offset=0,memo="no comments",productid0="0", warehouse0="", code0="", number0=0, productid1="0", warehouse1="", code1="", number1=0, productid2="0", warehouse2="", code2="", number2=0,productid3="0", warehouse3="", code3="", number3=0, productid4="0", warehouse4="", code4="", number4=0, productid5="0", warehouse5="", code5="", number5=0, productid6="0", warehouse6="", code6="", number6=0, productid7="0", warehouse7="", code7="", number7=0, productid8="0", warehouse8="", code8="", number8=0, productid9="0", warehouse9="", code9="", number9=0,color0=""):
        #self.productid = productid
        self.picture = picture
        self.orderdate = orderdate
        self.wangwang = wangwang
        self.cdeliverydate = cdeliverydate
        self.type1 = type1
        self.color0 = color0
        #self.number = number
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
        self.offset = offset
        self.memo = memo
        #self.warehouse = warehouse
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
    def __repr__(self):
        return self.id


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
    date = db.Column(db.DateTime, server_default = db.func.now())
    events = db.Column(db.VARCHAR(520))
    eventlevel = db.Column(db.String(80))
    user = db.Column(db.String(80))

    def __init__(self, events,eventlevel,user):
        self.events  = events
        self.eventlevel  = eventlevel
        self.user  = user

class Freight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    corpname = db.Column(db.String(80))
    deliveryplace = db.Column(db.String(80))
    destprovice = db.Column(db.String(80))
    destcity = db.Column(db.String(80))
    price = db.Column(db.Float)
    dropofffee = db.Column(db.Float)
    cheapest = db.Column(db.Float)
    transtype = db.Column(db.String(80))
    TBOST = db.Column(db.String(80))
    #发货地，目的省，目的市，每方价格，送货费，最低一票，快慢类型，自提时效

def __init__(self,corpname, deliveryplace,destprovice,destcity,price,dropofffee,cheapest,transtype,TBOST):
        self.corpname=corpname
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