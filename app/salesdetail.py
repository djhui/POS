#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
from app import app, lm
from sqlalchemy.sql import func
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from tools import *
from hashlib import sha512, md5
import os, json
from datetime import datetime
from dateutil.relativedelta import relativedelta
@app.route("/sales/detail",methods=['POST','GET'])
@login_required
def salesdetail():
    if request.method == 'POST':
        id = request.form['id']
        newsales = Sales.query.filter_by(id=id).first()

        if request.form['submit']=="update":
            transportation = request.form['transportation']
            try:Inprice = float(request.form['Inprice'])
            except:Inprice=None
            try:Aprice = float(request.form['Aprice'])
            except:Aprice=None
            try:Recashes = float(request.form['Recashes'])
            except:Recashes=None
            Commission = request.form['Commission']
            if Commission == "None":Commission=None
            deliverydate = request.form['deliverydate']
            trancorp = request.form['trancorp']
            Tnumber = request.form['Tnumber']
            memo = request.form['memo']
            newsales.transportation,newsales.Inprice,newsales.deliverydate,newsales.trancorp,newsales.Tnumber,newsales.Aprice,newsales.Recashes,newsales.Commission,newsales.memo = transportation, Inprice, deliverydate, trancorp, Tnumber, Aprice, Recashes, Commission, memo
            log = u"更新订单:%s" % id
        if request.form['submit']=="delete":
            log = memo = u"冲销订单%s" % newsales.id
            newsales.offset=1
            newsales.memo = memo
            for i in range(0, 10):
                if eval("newsales.productid%s" %i):
                    proinfo = Products.query.filter_by(id=eval("newsales.productid%s" %i)).first()
                    if eval("newsales.warehouse%s" %i) == "exstock" : proinfo.exstock = proinfo.exstock + eval("newsales.number%s" %i)
                    if eval("newsales.warehouse%s" %i) == "whstock" : proinfo.whstock = proinfo.whstock + eval("newsales.number%s" %i)
                    if eval("newsales.warehouse%s" %i) == "fastock" : proinfo.fastock = proinfo.fastock + eval("newsales.number%s" %i)
            db.session.add(Sales(newsales.picture,newsales.orderdate,newsales.wangwang,newsales.cdeliverydate,newsales.type1,newsales.address,newsales.transportation,newsales.Inprice,newsales.price,newsales.advprice,newsales.CSE,newsales.deliverydate,newsales.trancorp,newsales.Tnumber,newsales.Aprice,newsales.Recashes,newsales.Commission,newsales.offset,newsales.memo,newsales.productid0,newsales.warehouse0,newsales.code0,newsales.number0,newsales.productid1,newsales.warehouse1,newsales.code1,newsales.number1,newsales.productid2,newsales.warehouse2,newsales.code2,newsales.number2,newsales.productid3,newsales.warehouse3,newsales.code3,newsales.number3,newsales.productid4,newsales.warehouse4,newsales.code4,newsales.number4,newsales.productid5,newsales.warehouse5,newsales.code5,newsales.number5,newsales.productid6,newsales.warehouse6,newsales.code6,newsales.number6,newsales.productid7,newsales.warehouse7,newsales.code7,newsales.number7,newsales.productid8,newsales.warehouse8,newsales.code8,newsales.number8,newsales.productid9,newsales.warehouse9,newsales.code9,newsales.number9,newsales.color0))

            log = u"冲销订单:%s" % newsales.id
            db.session.add(Logs(log,u"销售管理",session['nickname'])) 
        if request.form['submit']=="getpro":
            allpro = []
            names = locals()
            for i in range(0, 10):
                if eval("newsales.productid%s" %i):
                    proinfo = Products.query.filter_by(id=eval("newsales.productid%s" %i)).first()
                    if eval("newsales.warehouse%s" %i) == u'exstock': warehouse = u"展厅"
                    if eval("newsales.warehouse%s" %i) == u'whstock': warehouse = u"仓库"
                    if eval("newsales.warehouse%s" %i) == u'fastock': warehouse = u"工厂"
                    result = {'id':eval("newsales.productid%s" %i),'picture':'<img src="../static/upload/'+proinfo.picture+'" width="200" />','products':proinfo.products,'specification':proinfo.specification,'color':proinfo.color,'warehouse':warehouse,'number':eval("newsales.number%s" %i)}
                    allpro.append(result)
            return json.dumps({'msg':allpro})
        db.session.commit()
    saleslist = db.session.query(Sales.id,Sales.picture,Sales.orderdate,Sales.wangwang,Sales.cdeliverydate,Sales.type1,Sales.color0,Sales.number0,Sales.address,Sales.transportation,Sales.Inprice,Sales.price,Sales.advprice,Sales.CSE,Sales.deliverydate,Sales.trancorp,Sales.Tnumber,Sales.Aprice,Sales.Recashes,Sales.Commission,Sales.memo,Sales.offset,Sales.productid1).all()
    prolist = Products.query.order_by(Products.id)
    delilist = Delivery.query.order_by(Delivery.id)
    translist = Trans.query.order_by(Trans.id)
    return render_template('sales_detail.html',session=session,nav = u"销售详情",saleslist=saleslist,delilist=delilist,catelist=g.catelist,translist=translist,prolist=prolist)
#--------------------------------------------------------------------------------------------------------------------