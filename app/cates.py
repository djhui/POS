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
#------------------------------categroies----------------------------------------
@app.route("/cates",methods=['POST','GET'])
@login_required
def cates():
    if request.method == 'POST':
        try:ecate=request.form['ecate']
        except:pass
        try:
            id=request.form['id']
            newcate = Cates.query.get(id)
        except:pass
        try:categroies=request.form['categroies']
        except:pass
        if request.form['submit']=="add":
            db.session.add(Cates(ecate,categroies))
            log = u"添加产品类别[%s-%s]" % ecate,categroies
        if request.form['submit']=="update":
            newcate.ecate = ecate
            newcate.categroies = categroies
            log = u"更新产品类别[%s->%s][%s->%s]" % (newcate.ecate,ecate,newcate.categroies,categroies)
        if request.form['submit']=="delete":
            log = u"删除产品类别[%s-%s]" % (newcate.ecate,newcate.categroies)
            db.session.delete(newcate)
        db.session.add(Logs(log,u"产品类别",session['nickname'])) 
        db.session.commit()

    return render_template('categroies.html',session=session,nav = u"产品分类",catelist=g.catelist)
