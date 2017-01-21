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
@lm.user_loader
def load_user(id):
    return User.query.filter_by(username=session['name']).first()
@app.before_request
def before_request():
    g.user = current_user
    g.catelist = Cates.query.order_by(Cates.id)
#----------------------------------------------------------------------
@app.route("/",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user != None and sha512(request.form['password']).hexdigest() == user.password: 
            login_user(user)
            session['id'] = user.id
            session['name'] = request.form['username']
            session['nickname'] = user.nickname
            return redirect(request.args.get('next') or url_for('main'))
        else:
            return render_template('error.html',error=u"用户名或者密码错误")
    return render_template('index.html')
 #----------------------------------------------------------------------
@app.route("/exit",methods=['POST','GET'])
@login_required
def exit():
    del session['name']
    logout_user()
    return redirect(url_for('login'))




@app.route("/log",methods=['POST','GET'])
@login_required
def log():
    loglist = Logs.query.order_by(Logs.id)
    return render_template('log.html',session=session,nav = u"操作日志",catelist=g.catelist,loglist=loglist)
#----------------------------------------------------------------------
