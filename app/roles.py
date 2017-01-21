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
@app.route("/roles",methods=['POST','GET'])
@login_required
def roles():
    if request.method == 'POST':
        try:
            id=request.form['id']
            newrole = Role.query.get(id)
        except:pass
        try:rolename = request.form['rolename']
        except:rolename="noname"
        try:sales = to_bool(request.form['sales'])
        except:sales=0
        try:salesdetail = to_bool(request.form['salesdetail'])
        except:salesdetail=0
        try:salesadd = to_bool(request.form['salesadd'])
        except:salesadd=0
        try:freight = to_bool(request.form['freight'])
        except:freight=0
        try:stock = to_bool(request.form['stock'])
        except:stock=0
        try:stockcabinets = to_bool(request.form['stockcabinets'])
        except:stockcabinets=0
        try:stockchairs = to_bool(request.form['stockchairs'])
        except:stockchairs=0
        try:stockdesks = to_bool(request.form['stockdesks'])
        except:stockdesks=0
        try:stocksofa = to_bool(request.form['stocksofa'])
        except:stocksofa=0
        try:stockadd = to_bool(request.form['stockadd'])
        except:stockadd=0
        try:account = to_bool(request.form['account'])
        except:account=0
        try:role = to_bool(request.form['role'])
        except:role=0
        print type(role)
        if request.form['submit']=="add":
            db.session.add(Role(rolename,sales,salesdetail,salesadd,freight,stock,stockcabinets,stockchairs,stockdesks,stocksofa,stockadd,account,role))
            log = u"添加角色:%s" % rolename
        if request.form['submit']=="update":
            newrole.sales,newrole.salesdetail,newrole.salesadd,newrole.freight,newrole.stock,newrole.stockcabinets,newrole.stockchairs,newrole.stockdesks,newrole.stocksofa,newrole.stockadd,newrole.account,newrole.role = sales,salesdetail,salesadd,freight,stock,stockcabinets,stockchairs,stockdesks,stocksofa,stockadd,account,role
            log = u"更改角色:%s" % newrole.rolename
        if request.form['submit']=="delete":
            db.session.delete(newrole)
            log = u"删除角色:%s" % newrole.rolename
        db.session.add(Logs(log,u"角色管理",session['nickname'])) 
        db.session.commit()
    rolelist = Role.query.order_by(Role.rolename)
    return render_template('roles.html',session=session,nav = u"角色管理",rolelist=rolelist,catelist=g.catelist)
#------------------------------categroies----------------------------------------