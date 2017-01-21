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
@app.route("/purchase", methods=['POST','GET'])
@login_required
def purchase():
    if request.method == 'POST':
        if request.form['submit']=="add":
            productid = request.form['productid']
            newpro = Products.query.filter_by(id=productid).first()
            products = request.form['products']
            code = request.form['code']
            specification = request.form['specification']
            color = request.form['color']
            exstock = int(request.form['exstock'])
            whstock = int(request.form['whstock'])
            fastock = int(request.form['fastock'])
            try:memo= request.form['memo']
            except:memo="no comments"
            db.session.add(Stock(productid,newpro.picture, products,code,specification,color,exstock,whstock,fastock,0,memo))
            stocklist = Stock.query.order_by(Stock.id)
            exstock += newpro.exstock
            whstock += newpro.whstock
            fastock += newpro.fastock
            newpro.exstock,newpro.whstock,newpro.fastock=exstock,whstock,fastock
            log = u"添加库存:ID->%s,产品名->%s,颜色->%s,展厅数量->%s,仓库数量->%s,工厂数量->%s" % (productid, products,color,exstock,whstock,fastock)
            db.session.add(Logs(log,u"采购产品",session['nickname'])) 
            db.session.commit()
            stocklist = Stock.query.order_by(Stock.id)
            return render_template('purlist.html',session=session,nav = u"采购订单记录",stocklist=stocklist,catelist=g.catelist)
    prolist = Products.query.order_by(Products.id)
    return render_template('purchase.html',session=session,nav = u"库存->新增",catelist=g.catelist, prolist = prolist)
#------------------------------------------------------------------------------------------------------------