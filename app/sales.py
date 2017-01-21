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
@app.route("/sales", methods=['POST','GET'])
@login_required
def sales():
    if request.method == 'POST':
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        SalesSum = []
        sumre = db.session.query(func.sum(Sales.price), func.sum(Sales.advprice), func.sum(Sales.Recashes)).filter("orderdate<=:enddate", "orderdate>=:startdate", "offset=:offset").params(startdate=startdate, enddate=enddate, offset=0).first()
        transfee = db.session.query(func.sum(Sales.Aprice)).filter("orderdate<=:enddate", "orderdate>=:startdate", "transportation not like :transportation", "offset=:offset").params(startdate=startdate, enddate=enddate, transportation=u"%到付%", offset=0).first()
        price = sumre[0] + sumre[1]
        result = {'id':1, 'employee':u"全店情况", 'price':"%.2f" % price, 'Aprice':"%.2f" %transfee[0] ,'Recashes':"%.2f" % sumre[2]}
        SalesSum.append(result)
        userlist = User.query.all()
        id=2
        for CSE in userlist:
            CSE = u"%s" % CSE.nickname
            try:
                sumre = db.session.query(func.sum(Sales.price),func.sum(Sales.advprice),func.sum(Sales.Recashes)).filter("CSE=:CSE","orderdate<=:enddate","orderdate>=:startdate","offset=:offset").params(CSE=CSE,startdate=startdate,enddate=enddate,offset=0).first()
                transfee = db.session.query(func.sum(Sales.Aprice)).filter("CSE=:CSE","orderdate<=:enddate","orderdate>=:startdate","transportation not like :transportation","offset=:offset").params(CSE=CSE,startdate=startdate,enddate=enddate,transportation=u"%到付%",offset=0).first()
            
                price = sumre[0] + sumre[1]
                result = {'id':id,'employee':CSE,'price':"%.2f" % price,'Aprice':"%.2f" %transfee[0] ,'Recashes':"%.2f" % sumre[2]}
                SalesSum.append(result)
            except:pass
            id +=1
        return json.dumps({'msg':SalesSum})
    nickname=User.query.order_by(User.username)
    return render_template('sales.html',session=session,nav = u"销售总览",catelist=g.catelist,nickname=nickname)
#---------------------------------------------------------------------------------------