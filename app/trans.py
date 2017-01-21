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

@app.route("/trans",methods=['POST','GET'])
@login_required
def trans():
    if request.method == 'POST':
        try:corpname = request.form['corpname']
        except:pass
        try:
            id=request.form['id']
            newcorp = Trans.query.get(id)
        except:pass
        if request.form['submit']=="add":
            db.session.add(Trans(corpname))
            log=u"添加物流公司[%s]" % (corpname)
        if request.form['submit']=="update":
            newcorp.corpname = corpname
            log=u"更新物流公司[%s]为[%s]" % (newcorp.corpname,corpname)
        if request.form['submit']=="delete":
            db.session.delete(newcorp)
            log=u"删除物流公司%s" % newcorp.corpname
        db.session.add(Logs(log,u"物流公司",session['nickname'])) 
        db.session.commit()
    translist = Trans.query.order_by(Trans.id)
    return render_template('transcorp.html',session=session,nav = u"物流公司",translist=translist,catelist=g.catelist)