#!/usr/bin/python
# -*- coding:utf-8 -*-
from app import app,db
from app.models import Sales, Products
for i in range(0, 500):
    #print sales.productid0
    sales = db.session.query(Sales).filter_by(id=i).first()
    try:
        pro = db.session.query(Products).filter_by(id=sales.productid0).first()
        sales.type1 = pro.specification
        sales.color0 = pro.color
        db.session.commit()
    except:pass
