#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import * 
from app import app,lm
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from hashlib import sha512
import os
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',methods=['POST','GET'],error=u"文件未找到"), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('404.html',methods=['POST','GET']), 403

@lm.user_loader
def load_user(id):
    return User.query.filter_by(username=session['name']).first()
    

@app.before_request
def before_request():
    g.user = current_user
    g.catelist = Cates.query.order_by(Cates.id)

@app.route("/",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        
        if user != None and sha512(request.form['password']).hexdigest() == user.password: 
            login_user(user)
            session['name'] = request.form['username']
            session['nickname'] = user.nickname
            return redirect(request.args.get('next') or url_for('main'))
        else:
            return render_template('error.html',error=u"用户名或者密码错误")
    return render_template('index.html')
 
@app.route("/exit",methods=['POST','GET'])
@login_required
def exit():
    
    del session['name']
    logout_user()
    return redirect(url_for('login'))


@app.route("/main",methods=['POST','GET'])
@login_required
def main():
    
    return render_template('main.html',user=g.user,catelist=g.catelist)

@app.route("/sales",methods=['POST','GET'])
@login_required
def sales():
    return render_template('sales.html',session=session,nav = u"销售总览",catelist=g.catelist)

@app.route("/sales/detail",methods=['POST','GET'])
@login_required
def salesdetail():
    saleslist = Sales.query.order_by(Sales.id)
    return render_template('sales_detail.html',session=session,nav = u"销售详情",saleslist=saleslist,catelist=g.catelist)

@app.route("/sales/add",methods=['POST','GET'])
@login_required
def salesadd():
    if request.method == 'POST':
        if request.form['submit']=="add":
            picture = request.form['picture']
            orderdate = request.form['orderdate']
            wangwang = request.form['wangwang']
            cdeliverydate = request.form['cdeliverydate']
            type = request.form['type']
            color = request.form['color']
            number = int(request.form['number'])
            address = request.form['address']
            transportation = request.form['transportation']
            Inprice = float(request.form['Inprice'])
            price = float(request.form['price'])
            advprice = float(request.form['advprice'])
            CSE = request.form['CSE']
            deliverydate = request.form['deliverydate']
            trancorp = request.form['trancorp']
            Tnumber = request.form['Tnumber']
            Aprice = float(request.form['Aprice'])
            Recashes = float(request.form['Recashes'])
            Commission = request.form['Commission']
            try:memo = request.form['memo']
            except:memo="no comments"
            addsales = Sales(picture, orderdate, wangwang, cdeliverydate, type,color,number,address,transportation,Inprice,price,advprice,CSE,deliverydate, trancorp, Tnumber, Aprice,Recashes,Commission, memo)
            db.session.add(addsales)
            db.session.commit()
    nickname=User.query.order_by(User.username)
    delilist = Delivery.query.order_by(Delivery.id)
    translist = Trans.query.order_by(Trans.id)
    return render_template('salesadd.html',session=session,nav = u"添加",nickname=nickname,delilist=delilist,catelist=g.catelist,translist=translist)

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
        if request.form['submit']=="update":
            if request.form['password']:newuser.password=password
            newuser.nickname, newuser.mobile, newuser.role =nickname, mobile, role
        if request.form['submit']=="delete":
            db.session.delete(newuser)
        db.session.commit()
    userlist = User.query.order_by(User.username)
    rolelist = Role.query.order_by(Role.rolename)
    return render_template('users.html',session=session,nav = u"用户管理",userlist=userlist,rolelist=rolelist,catelist=g.catelist)

@app.route("/freight",methods=['POST','GET'])
@login_required
def freight():
    return render_template('freight.html',session=session,nav = u"运费估算",catelist=g.catelist)

@app.route("/stocks",methods=['POST','GET'])
@login_required
def stocks():
    stocklist = Stock.query.order_by(Stock.id)
    return render_template('stocks.html',session=session,nav = u"库存总览",stocklist=stocklist,catelist=g.catelist)

#------------------------------------------------------------------------------------------------------------
@app.route("/stocks/<postcate>",methods=['POST','GET'])
@login_required
def postcate(postcate):
    cate1 = Cates.query.filter_by(ecate=postcate).first()
    stocklist = Stock.query.filter_by(categroies=cate1.categroies).all()
    return render_template('stocks.html',session=session,nav = cate1.categroies,stocklist=stocklist,catelist=g.catelist)
#------------------------------------------------------------------------------------------------------------


@app.route("/stocks/add",methods=['POST','GET'])
@login_required
def stocksadd():
    if request.method == 'POST':
        if request.form['submit']=="add":
            picture = request.form['picture']
            products = request.form['products']
            code = request.form['code']
            specification = request.form['specification']
            color = request.form['color']
            exstock = int(request.form['exstock'])
            whstock = int(request.form['whstock'])
            fastock = int(request.form['fastock'])
            pkgsize = request.form['pkgsize']
            pgkbulk = request.form['pgkbulk']
            categroies = request.form['categroies']
            try:memo= request.form['memo']
            except:memo="no comments"
            addstock = Stock(picture, products,categroies,code,specification,color,exstock,whstock,fastock,pkgsize,pgkbulk,memo)
            db.session.add(addstock)
            db.session.commit()
    return render_template('stocksadd.html',session=session,nav = u"库存->新增",catelist=g.catelist)
#------------------------------------------------------------------------------------------------------------
@app.route("/roles",methods=['POST','GET'])
@login_required
def roles():
    if request.method == 'POST':
        try:
            id=request.form['id']
            newrole = Role.query.get(id)
        except:pass
        try:rolename = request.form['rolename']
        except:pass
        try:sales = int(request.form['sales'])
        except:sales = False
        try:salesdetail = int(request.form['salesdetail'])
        except:salesdetail = False
        try:salesadd = int(request.form['salesadd'])
        except:salesadd = False
        try:freight = int(request.form['freight'])
        except:freight = False
        try:stock = int(request.form['stock'])
        except:stock = False
        try:stockcabinets = int(request.form['stockcabinets'])
        except:stockcabinets = False
        try:stockchairs = int(request.form['stockchairs'])
        except:stockchairs = False
        try:stockdesks = int(request.form['stockdesks'])
        except:stockdesks = False
        try:stocksofa = int(request.form['stocksofa'])
        except:stocksofa = False
        try:stockadd = int(request.form['stockadd'])
        except:stockadd = False
        try:account = int(request.form['account'])
        except:account = False
        try:role = int(request.form['role'])
        except:role = False
        if request.form['submit']=="add":
            db.session.add(Role(rolename,sales,salesdetail,salesadd,freight,stock,stockcabinets,stockchairs,stockdesks,stocksofa,stockadd,account,role))
        if request.form['submit']=="update":
            newrole.sales,newrole.salesdetail,newrole.salesadd,newrole.freight,newrole.stock,newrole.stockcabinets,newrole.stockchairs,newrole.stockdesks,newrole.stocksofa,newrole.stockadd,newrole.account,newrole.role = sales,salesdetail,salesadd,freight,stock,stockcabinets,stockchairs,stockdesks,stocksofa,stockadd,account,role
        if request.form['submit']=="delete":
            db.session.delete(newrole)
        db.session.commit()
    rolelist = Role.query.order_by(Role.rolename)
    return render_template('roles.html',session=session,nav = u"角色管理",rolelist=rolelist,catelist=g.catelist)

#------------------------------categroies----------------------------------------
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
        if request.form['submit']=="update":
            newcorp.corpname = corpname
        if request.form['submit']=="delete":
            db.session.delete(newcorp)
        db.session.commit()
    translist = Trans.query.order_by(Trans.id)
    return render_template('transcorp.html',session=session,nav = u"物流公司",translist=translist,catelist=g.catelist)

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
        if request.form['submit']=="update":
            newcate.ecate = ecate
            newcate.categroies = categroies
        if request.form['submit']=="delete":
            
            db.session.delete(newcate)
        db.session.commit()

    return render_template('categroies.html',session=session,nav = u"产品分类",catelist=g.catelist)
#------------------------------delivery----------------------------------------
@app.route("/delivery",methods=['POST','GET'])
@login_required
def delivery():
    if request.method == 'POST':
        try:delivery = request.form['delivery']
        except:pass
        try:
            id = request.form['id']
            newdeli = Delivery.query.get(id)
        except:pass
        if request.form['submit']=="add":
            db.session.add(Delivery(delivery))
        if request.form['submit']=="update":
            newdeli.delivery = delivery
        if request.form['submit']=="delete":
            db.session.delete(newdeli)
        db.session.commit()
    delilist = Delivery.query.order_by(Delivery.id)
    return render_template('delivery.html',session=session,nav = u"送货方式",delilist=delilist,catelist=g.catelist)
#----------------------------------------------------------------------
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['files[]']
        filename = f.filename
        minetype = f.content_type
        f.save(os.getcwd()+'/app/static/upload/' + filename) 
        return json.dumps({"files": [{"name": filename, "minetype": minetype}]})