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
#------------------------------delivery----------------------------------------
@app.route("/delivery",methods=['POST','GET'])
@login_required
def delivery():
    if request.method == 'POST':
        try:delivery = request.form['delivery']
        except:pass
        try:
            id = request.form['id']
            newdeli = Delivery.query.get(id)
        except:pass
        if request.form['submit']=="add":
            db.session.add(Delivery(delivery))
            log = u"添加送货方式[%s]" % delivery
        if request.form['submit']=="update":
            newdeli.delivery = delivery
            log = u"更新送货方式[%s->%s]" % (newdeli.delivery,delivery)
        if request.form['submit']=="delete":
            db.session.delete(newdeli)
            log = u"删除送货方式[%s]" % newdeli.delivery
        db.session.add(Logs(log,u"送货方式",session['nickname'])) 
        db.session.commit()
    delilist = Delivery.query.order_by(Delivery.id)
    return render_template('delivery.html',session=session,nav = u"送货方式",delilist=delilist,catelist=g.catelist)
#----------------------------------------------------------------------