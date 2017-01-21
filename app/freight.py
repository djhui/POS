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
@app.route("/freight",methods=['POST','GET'])
@login_required
def freight():
    Cals = []
    if request.method == 'POST':
        try:
            id = request.form['id']
            Transfee = Products.query.filter_by(id=id).first()
        except:pass
        deliverycity = request.form['deliverycity']
        trancorp = request.form['trancorp']
        cho_Province = request.form['cho_Province']
        cho_City = request.form['cho_City']
        cho_Area = request.form['cho_Area']
        transportation = request.form['transportation'].split("-")[-1]
        number = int(request.form['number'])
        discount = float(request.form['discount'])
        wooden = request.form['wooden']
        bulk = request.form['bulk']
        transtype = request.form['transtype']

        if bulk:
            bulk=float(bulk) * number
            product = u"自定义"
            pkgsize = u"无所谓~"
        else:
            bulk=float(Transfee.pkgbulk) * number
            product = Transfee.products
            pkgsize = Transfee.pkgsize
        if wooden == "yes":wooden = 200
        else:wooden =0
        if trancorp =="all":
            transcorps = Freight.query.filter_by(deliveryplace=deliverycity,destcity=cho_Area,transtype=transtype).all()
            if not transcorps:
                transcorps = Freight.query.filter_by(deliveryplace=deliverycity,destcity=cho_City,transtype=transtype).all()
                if not transcorps:
                    transcorps = Freight.query.filter_by(deliveryplace=deliverycity,destcity=cho_Province,transtype=transtype).all()
        else:
            transcorps = Freight.query.filter_by(corpname=trancorp, deliveryplace=deliverycity, destcity=cho_Area,transtype=transtype).all()
            if not transcorps:
                transcorps = Freight.query.filter_by(deliveryplace=deliverycity,destcity=cho_City,corpname=trancorp,transtype=transtype).all()
                if not transcorps:
                    transcorps = Freight.query.filter_by(deliveryplace=deliverycity,destcity=cho_Province,transtype=transtype).all()
        if transcorps:
            for tran in transcorps:
                woodenfee = bulk * wooden
                totalprice = bulk * tran.price * discount 
                if totalprice < tran.cheapest:totalprice = tran.cheapest 
                if transportation != u"自提":
                    totalprice = totalprice + tran.dropofffee + woodenfee
                else:
                    totalprice = totalprice  + woodenfee
                result = {'product':product,'pkgsize':pkgsize,'price':tran.price,'pkgbulk':bulk,'transcorp':tran.corpname,'transtype':tran.transtype,'delicity':tran.deliveryplace,'TBOST':tran.TBOST,'destcity':tran.destcity,'fee':"%.2f" % totalprice}
                
                Cals.append(result)
                #print json.dumps(Cals)
            
            return json.dumps({'msg':Cals})
        else:
            return json.dumps({"msg":"None"})
    #总运费=price*体积*0.8+dropofffee，
    #如果price*体积*0.8<cheapest，
    #总运费=cheapest+dropofffe
    #查运费的时候，物流公司输入框默认项为“全部”，默认显示全部物流公司运费 
    #木架费是200元/m³
    #发货方式如果选的是自提，就直接是price*体积*折扣，不用加dropofffee了
    translist = Trans.query.order_by(Trans.id)
    delilist = Delivery.query.order_by(Delivery.id)
    prolist = Products.query.order_by(Products.id)
    return render_template('freight.html',session=session,nav = u"运费估算",catelist=g.catelist,delilist=delilist,translist =translist,prolist =prolist)
