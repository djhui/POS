#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/flask'
db = SQLAlchemy(app)
 
class User(db.Model): #帐号表
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True) #用户名
    nickname = db.Column(db.String(80)) #别名
    mobile = db.Column(db.String(80)) #手机
    password = db.Column(db.String(320)) #密码
    role = db.Column(db.String(32), unique=True) #角色
  
    def __init__(self, username, password, role, mobile, nickname):
        self.username = username
        self.password = password
        self.role= role
        self.mobile = mobile
        self.nickname = nickname

class Role(db.Model): #角色表,默认表示相对应的权限
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(80), unique=True) #角色名
    sales = db.Column(db.Boolean(1)) #销售
    salesdetail = db.Column(db.Boolean(1)) #销售详情
    salesadd = db.Column(db.Boolean(1)) #销售添加
    freight = db.Column(db.Boolean(1)) #运费
    stock = db.Column(db.Boolean(1)) #库存
    stockcabinets = db.Column(db.Boolean(1)) #库存,柜
    stockchairs = db.Column(db.Boolean(1)) #库存,椅
    stockdesks = db.Column(db.Boolean(1)) #库存,桌
    stocksofa = db.Column(db.Boolean(1)) #库存,沙发
    stockadd = db.Column(db.Boolean(1)) #库存,添加
    account = db.Column(db.Boolean(1))  #帐号
    role = db.Column(db.Boolean(1)) #角色
  
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

class Stock(db.Model): #库存表
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.VARCHAR(520), unique=True) #图片
    products = db.Column(db.String(120), unique=True) #产品名称
    exstock = db.Column(db.Integer) #展厅数量
    whstock = db.Column(db.Integer) #仓库数量
    fastock = db.Column(db.Integer) #工厂数量
    memo = db.Column(db.VARCHAR(520)) #备注
  
    def __init__(self, picture="0", products="0", exstock=0,whstock=0,fastock=0,memo="no comments"):
        self.picture = picture
        self.products = products
        self.exstock = exstock
        self.whstock = whstock
        self.fastock = fastock
        self.memo = memo

class Products(db.Model): #产品表
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.VARCHAR(520), unique=True) #图片
    products = db.Column(db.String(120), unique=True) #产品名
    categroies = db.Column(db.String(120)) #规格
    code = db.Column(db.String(120)) #代码
    specification = db.Column(db.String(120)) #分类 
    pkgsize = db.Column(db.String(120)) #包装尺寸
    pgkbulk = db.Column(db.String(120)) #包装体积
    memo = db.Column(db.VARCHAR(520)) #备注
  
    def __init__(self, picture="0", products="0", categroies="0", code="0", specification="0",pkgsize="0*0*0",pgkbulk="6",memo="no comments"):
        self.picture = picture
        self.products = products
        self.categroies = categroies
        self.code = code
        self.specification = specification
        self.pkgsize = pkgsize
        self.pgkbulk = pgkbulk
        self.memo = memo

class Sales(db.Model): #销售表
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.VARCHAR(520), unique=True) #图片
    orderdate = db.Column(db.Date) #下单日期
    wangwang = db.Column(db.String(120)) #旺旺
    cdeliverydate = db.Column(db.Date) #Cumstomer wants to delivery data,客户要求发货日期
    type = db.Column(db.String(120)) #
    color = db.Column(db.String(120)) #颜色 
    number = db.Column(db.Integer) #数量 写错了,当时 应该是Qty
    address = db.Column(db.VARCHAR(520)) #发货地址
    trancorp = db.Column(db.VARCHAR(520)) #物流公司
    transportation = db.Column(db.VARCHAR(520)) #
    Inprice = db.Column(db.Float) #Insurance price 保费
    price = db.Column(db.Float) #sales price 销售价格
    advprice = db.Column(db.Float) #Advance fee 预付费
    CSE = db.Column(db.String(120)) #Customer Service Employee 客服
    deliverydate = db.Column(db.Date) #actual delivery date 实际发货日期
    Tnumber = db.Column(db.String(120)) #transportation number 物流单号
    Aprice = db.Column(db.Float) #Actual price 实际费用
    Recashes = db.Column(db.Float) #Cash back 返现
    Commission = db.Column(db.Date) #结算
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


class Trans(db.Model): #物流公司
    id = db.Column(db.Integer, primary_key=True)
    corpname = db.Column(db.String(80), unique=True) #公司名字
   
  
    def __init__(self, corpname):
        self.corpname = corpname

class Cates(db.Model): #产品类别
    id = db.Column(db.Integer, primary_key=True)
    ecate = db.Column(db.String(80), unique=True) #英文名,类别
    categroies = db.Column(db.String(80), unique=True) #中文名,类别

    def __init__(self, ecate,categroies):
        self.ecate=ecate
        self.categroies = categroies

class Delivery(db.Model): #送货方式
    id = db.Column(db.Integer, primary_key=True)
    delivery = db.Column(db.String(80), unique=True) #送货方式

    def __init__(self, delivery):
        self.delivery = delivery

class Logs(db.Model): #日志
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, server_default = db.func.now()) #日期时间
    events = db.Column(db.VARCHAR(520)) #事件
    eventlevel = db.Column(db.String(80)) #事件级别
    user = db.Column(db.String(80)) #操作人

    def __init__(self, events,eventlevel,user):
        self.events  = events
        self.eventlevel  = eventlevel
        self.user  = user

class Freight(db.Model): #运费
    id = db.Column(db.Integer, primary_key=True)
    corpname = db.Column(db.String(80))    #
    deliveryplace = db.Column(db.String(80)) #发货地
    destprovice = db.Column(db.String(80)) #目的省
    destcity = db.Column(db.String(80)) #目的市
    price = db.Column(db.Float) #价格
    dropofffee = db.Column(db.Float) #送货费
    cheapest = db.Column(db.Float) #最低一票
    transtype = db.Column(db.String(80)) #快慢类型
    TBOST = db.Column(db.String(80)) #自提
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