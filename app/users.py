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

@app.route("/users",methods=['POST','GET'])
@login_required
def users():
    if request.method == 'POST':
        try:
            id = request.form['id']
            newuser = User.query.get(id)
        except:pass
        try:username = request.form['username']
        except:pass
        try:password = sha512(request.form['password']).hexdigest()
        except:pass
        try:nickname = request.form['nickname']
        except:pass
        try:mobile = request.form['mobile']
        except:pass
        try:role = request.form['role']
        except:pass
        if request.form['submit']=="add":
            db.session.add(User(username, password, role,mobile, nickname))
            log = u"添加用户:%s-角色:%s-手机:%s-别名:%s" % (username,role,mobile,nickname)
        if request.form['submit']=="update":
            if request.form['password']:
                newuser.password=password
                log = u"更新用户%s的信息为-角色:%s,手机:%s-别名:%s,以及密码(此处不显示)" % (username,role,mobile,nickname)
            newuser.nickname, newuser.mobile, newuser.role =nickname, mobile, role
            log = u"更新用户%s的信息为-角色:%s,手机:%s-别名:%s" % (username,role,mobile,nickname)
        if request.form['submit']=="uppswd":
            newuser.password=password
            log = u"%s更改了密码" % (newuser.username)
        if request.form['submit']=="delete":
            db.session.delete(newuser)
            log = u"删除用户:%s" % (newuser.username)
        db.session.add(Logs(log,u"用户管理",session['nickname'])) 
        db.session.commit()
        
    userlist = User.query.order_by(User.username)
    rolelist = Role.query.order_by(Role.rolename)
    return render_template('users.html',session=session,nav = u"用户管理",userlist=userlist,rolelist=rolelist,catelist=g.catelist)
#----------------------------------------------------------------------