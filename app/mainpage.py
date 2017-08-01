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

#----------------------------------------------------------------------
@app.route("/main", methods=['POST','GET'])
@login_required
def main():
    if request.method == 'POST':
        Maindata = []
        for i in range(5,-1,-1):
            label = (datetime.now() - relativedelta(months=i)).strftime("%Y-%b")
            date = (datetime.now() - relativedelta(months=i)).strftime("%Y-%m")
            try:
                sumre = db.session.query(func.sum(Sales.price), func.sum(Sales.advprice), func.sum(Sales.Recashes)).filter("orderdate like :date", "offset=:offset").params(date=date+"%", offset=0).first()
                sales = sumre[0] + sumre[1]
                Recashes = sumre[2]
                if sales == None:sales = 0
                if Recashes == None:Recashes = 0
            except:
                Recashes = sales = 0
            try:
                transfee = db.session.query(func.sum(Sales.Aprice)).filter("orderdate like :date", "transportation not like :transportation", "offset=:offset").params(date=date+"%", transportation=u"%到付%", offset=0).first()
                if transfee[0] == None:
                    Aprice = 0
                else: Aprice = transfee[0]
            except:Aprice = 0
            salesprice = sales - Aprice - Recashes
            result = {'id':i,'label':label,'sales':"%.2f" % salesprice}
            Maindata.append(result)

        date1 = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d")
        date2 = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m-01")
        try:
            sumre = db.session.query(func.sum(Sales.price), func.sum(Sales.advprice), func.sum(Sales.Recashes)).filter("orderdate<=:date1","orderdate>=:date2", "offset=:offset").params(date1=date1,date2=date2, offset=0).first()
            sales = sumre[0] + sumre[1]
            Recashes = sumre[2]
            if sales == None: sales = 0
            if Recashes == None: Recashes = 0
        except:
            Recashes = sales = 0
        try:
            transfee = db.session.query(func.sum(Sales.Aprice)).filter("orderdate<=:date1","orderdate>=:date2", "transportation not like :transportation", "offset=:offset").params(date1=date1,date2=date2, transportation=u"%到付%", offset=0).first()
            if transfee[0] == None:
                Aprice = 0
            else: Aprice = transfee[0]
        except:Aprice = 0
        salesprice1 = sales - Aprice - Recashes
        try:salepct = (salesprice - salesprice1) / salesprice1 * 100
        except:salepct =0
        return json.dumps({'msg':Maindata,'msg1': "%.2f" % salesprice1,'msg2': "%.2f" % salepct})

    return render_template('main.html', user=g.user, catelist=g.catelist)
#----------------------------------------------------------------------