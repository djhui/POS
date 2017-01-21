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
@app.route("/purlist",methods=['POST','GET'])
@login_required
def purlist():
    if request.method == 'POST':
        try:
            id = request.form['id']
            newstock = Stock.query.get(id)
            newpro = Products.query.filter_by(id=newstock.productid).first()
        except:pass
        if request.form['submit']=="delete":
            newstock.offset=1
            memo=u"冲销订单%s" % id
            db.session.add(Stock(newstock.productid,newstock.picture,newstock.products,newstock.code,newstock.specification,newstock.color,newstock.exstock,newstock.whstock,newstock.fastock,newstock.offset,memo))
            newpro.exstock = newpro.exstock - newstock.exstock
            newpro.whstock = newpro.whstock - newstock.whstock
            newpro.fastock = newpro.fastock - newstock.fastock
            log = memo
        db.session.add(Logs(log,u"采购产品",session['nickname'])) 
        db.session.commit()
    stocklist = Stock.query.order_by(Stock.id)
    return render_template('purlist.html',session=session,nav = u"采购订单记录",stocklist=stocklist,catelist=g.catelist)
#------------------------------------------------------------------------------------------------------------