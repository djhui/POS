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
@app.route("/salesorder",methods=['POST','GET'])
@login_required
def salesorder():
    names = locals()
    if request.method == 'POST':
        for i in xrange(0, 10):
            try:
                names['productid%s' % i] = request.form['productid%s' % i]
                names['number%s' % i] = int(request.form['number%s' % i])
                names['warehouse%s' % i] = request.form['warehouse%s' % i]
                names['code%s' % i] = request.form['code%s' % i]
                names['color%s' % i] = request.form['color%s' % i]
                print names['productid%s' % i]
                newpro = Products.query.filter_by(id=names['productid%s' % i]).first()
                picture = newpro.picture
            except:
                names['productid%s' % i] = names['number%s' % i] = names['warehouse%s' % i] = names['code%s' % i] = names['color%s' % i] = None
            if names['warehouse%s' % i] == "exstock" : newpro.exstock = newpro.exstock - names['number%s' % i]
            if names['warehouse%s' % i] == "whstock" : newpro.whstock = newpro.whstock - names['number%s' % i]
            if names['warehouse%s' % i] == "fastock" : newpro.fastock = newpro.fastock - names['number%s' % i]
        orderdate = request.form['orderdate']
        wangwang = request.form['wangwang']
        cdeliverydate = request.form['cdeliverydate']
        type1 = request.form['specification0']
        color = request.form['color0']
        warehouse = number = transportation = Inprice = deliverydate = trancorp = Tnumber = Aprice = Recashes = Commission = None 

        address = request.form['address']
        price = float(request.form['price'])
        advprice = float(request.form['advprice'])
        CSE = request.form['CSE']
        offset = 0
        try:memo = request.form['memo']
        except:memo="no comments"
        if request.form['submit']=="add":
            addsales = Sales(picture,orderdate, wangwang, cdeliverydate, type1,address,transportation,Inprice,price,advprice,CSE,deliverydate, trancorp, Tnumber, Aprice,Recashes,Commission,offset,memo,names['productid0'], names['warehouse0'], names['code0'], names['number0'], names['productid1'], names['warehouse1'], names['code1'], names['number1'], names['productid2'], names['warehouse2'], names['code2'], names['number2'],names['productid3'], names['warehouse3'], names['code3'], names['number3'], names['productid4'], names['warehouse4'], names['code4'], names['number4'], names['productid5'], names['warehouse5'], names['code5'], names['number5'], names['productid6'], names['warehouse6'], names['code6'], names['number6'], names['productid7'], names['warehouse7'], names['code7'], names['number7'], names['productid8'], names['warehouse8'], names['code8'], names['number8'], names['productid9'], names['warehouse9'], names['code9'], names['number9'],color)
            db.session.add(addsales)
            log = u"添加订单:产品ID->%s,下单日期->%s,旺旺->%s,客户要求发货日期->%s,规格->%s,颜色->%s,发货仓库->%s,下单数量->%s,发货地址->%s,物流送货方式->%s,保费->%s,商品价格->%s,预收运费->%s,客服->%s,实际发货日期->%s,物流公司->%s,物流单号->%s,,实际运费->%s,返现->%s,提成结算日期->%s,备注->%s" % (names['productid0'],orderdate,wangwang,cdeliverydate,type1,names['color0'],names['warehouse0'],names['number0'],address,transportation,Inprice,price,advprice,CSE,deliverydate,trancorp,Tnumber,Aprice,Recashes,Commission,memo)
        db.session.add(Logs(log,u"销售订单",session['nickname'])) 
        db.session.commit()
    nickname=User.query.order_by(User.username)
    prolist = Products.query.order_by(Products.id)
    return render_template('salesorder.html',session=session,nav = u"添加",nickname=nickname,catelist=g.catelist,prolist=prolist)
#----------------------------------------------------------------------