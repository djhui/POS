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


@app.route("/stocks",methods=['POST','GET'])
@login_required
def stocks():
    stocklist = Products.query.order_by(Products.id)
    return render_template('stocks.html',session=session,nav = u"库存总览",stocklist=stocklist,catelist=g.catelist)

#------------------------------------------------------------------------------------------------------------
@app.route("/stocks/<postcate>",methods=['POST','GET'])
@login_required
def postcate(postcate):
    cate1 = Cates.query.filter_by(ecate=postcate).first()
    stocklist = Products.query.filter_by(categroies=cate1.categroies).all()
    return render_template('stocks.html',session=session,nav = cate1.categroies,stocklist=stocklist,catelist=g.catelist)
#------------------------------------------------------------------------------------------------------------