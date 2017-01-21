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
@app.route("/products",methods=['POST','GET'])
@login_required
def products():
    if request.method == 'POST':
        try:
            id = request.form['id']
            newpro = Products.query.get(id)
        except:pass
        try:picture = request.form['picture']
        except:pass
        try:products = request.form['products']
        except:pass
        try:code = request.form['code']
        except:pass
        try:specification = request.form['specification']
        except:pass
        try:color = request.form['color']
        except:pass
        try:pkgsize = request.form['pkgsize']
        except:pass
        try:pkgbulk = float(request.form['pkgbulk'])
        except:pass
        try:categroies = request.form['categroies']
        except:pass
        try:memo= request.form['memo']
        except:pass
        if request.form['submit']=="add":
            exstock=0
            whstock=0
            fastock=0
            db.session.add(Products(picture,products,categroies,code,specification,color,exstock,whstock,fastock,pkgsize,pkgbulk,memo))
            log = u"新建产品:产品图片->%s,名称->%s,规格->%s,编号->%s,包装尺寸->%s,包装体积->%s,类别->%s,备注->%s" % (picture,products,categroies,code,specification,pkgsize,pkgbulk,memo)
        if request.form['submit']=="update":
            if request.form['picture']:
                newpro.picture=picture
            newpro.products, newpro.code, newpro.specification, newpro.pkgsize, newpro.pkgbulk, newpro.categroies,newpro.memo  = products, code, specification, pkgsize, pkgbulk, categroies, memo
            log = u"更改产品:名称->%s,规格->%s,编号->%s,包装尺寸->%s,包装体积->%s,类别->%s,备注->%s" % (products,categroies,code,specification,pkgsize,pkgbulk,memo)
        if request.form['submit']=="delete":
            db.session.delete(newpro)
            log = u"删除产品:名称->%s,规格->%s,编号->%s,包装尺寸->%s,包装体积->%s,类别->%s,备注->%s" % (newpro.products,newpro.categroies,newpro.code,newpro.specification,newpro.pkgsize,newpro.pkgbulk,newpro.memo)
        db.session.add(Logs(log,u"产品管理",session['nickname']))
        db.session.commit()
    prolist = Products.query.order_by(Products.id)
    return render_template('products.html',session=session,nav = u"全部产品",catelist=g.catelist,prolist=prolist)