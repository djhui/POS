#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import * 
from app import app,lm
from flask_login import login_user, logout_user, current_user, login_required
from models import User,Role,db,Sales,Stock,Trans,Cates,Delivery
from hashlib import sha512
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',methods=['POST','GET']), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('404.html',methods=['POST','GET']), 403

@lm.user_loader
def load_user(id):
    return User.query.filter_by(username=session['name']).first()

@app.before_request
def before_request():
    g.user = current_user

@app.route("/",methods=['POST','GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        session['name'] = request.form['username']
        session['nickname'] = user.nickname
        if request.form['username'] == user.username and sha512(request.form['password']).hexdigest() == user.password: 
            login_user(user)
            return redirect(request.args.get('next') or url_for('main'))
    return render_template('index.html')
 
@app.route("/exit",methods=['POST','GET'])
@login_required
def exit():
    
    session['name']=None
    logout_user()
    return redirect(url_for('login'))


@app.route("/main",methods=['POST','GET'])
@login_required
def main():
    user = current_user
    catelist = Cates.query.order_by(Cates.id)
    return render_template('main.html',user=user,catelist=catelist)

@app.route("/sales",methods=['POST','GET'])
@login_required
def sales():
    catelist = Cates.query.order_by(Cates.id)
    return render_template('sales.html',session=session,nav = u"销售总览",catelist=catelist)

@app.route("/sales/detail",methods=['POST','GET'])
@login_required
def salesdetail():
    saleslist = Sales.query.order_by(Sales.id)
    catelist = Cates.query.order_by(Cates.id)
    return render_template('sales_detail.html',session=session,nav = u"销售详情",saleslist=saleslist,catelist=catelist)

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
    catelist = Cates.query.order_by(Cates.id)
    translist = Trans.query.order_by(Trans.id)
    return render_template('salesadd.html',session=session,nav = u"添加",nickname=nickname,delilist=delilist,catelist=catelist,translist=translist)

@app.route("/users",methods=['POST','GET'])
@login_required
def users():
    if request.method == 'POST':
        if request.form['submit']=="add":
            username = request.form['username']
            password = sha512(request.form['password']).hexdigest()
            nickname = request.form['nickname']
            mobile = request.form['mobile']
            role = request.form['role']

            adduser=User(username=username, password=password, role=role,nickname=nickname,mobile=mobile)
            db.session.add(adduser)
            db.session.commit()



    userlist = User.query.order_by(User.username)
    rolelist = Role.query.order_by(Role.rolename)
    catelist = Cates.query.order_by(Cates.id)
    return render_template('users.html',session=session,nav = u"用户管理",userlist=userlist,rolelist=rolelist,catelist=catelist)

@app.route("/freight",methods=['POST','GET'])
@login_required
def freight():
    catelist = Cates.query.order_by(Cates.id)
    return render_template('freight.html',session=session,nav = u"运费估算",catelist=catelist)

@app.route("/stocks",methods=['POST','GET'])
@login_required
def stocks():
    stocklist = Stock.query.order_by(Stock.id)
    catelist = Cates.query.order_by(Cates.id)
    return render_template('stocks.html',session=session,nav = u"库存总览",stocklist=stocklist,catelist=catelist)

#------------------------------------------------------------------------------------------------------------
@app.route("/stocks/<postcate>",methods=['POST','GET'])
@login_required
def postcate(postcate):
    cate1 = Cates.query.filter_by(ecate=postcate).first()
    stocklist = Stock.query.filter_by(categroies=cate1.categroies).all()
    catelist = Cates.query.order_by(Cates.id)
    return render_template('stocks.html',session=session,nav = cate1.categroies,stocklist=stocklist,catelist=catelist)
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
    catelist = Cates.query.order_by(Cates.id)
    return render_template('stocksadd.html',session=session,nav = u"库存->新增",catelist=catelist)

@app.route("/roles",methods=['POST','GET'])
@login_required
def roles():
    if request.method == 'POST':
        if request.form['submit']=="add":
            rolename = request.form['rolename']
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
            addrole = Role(rolename,sales,salesdetail,salesadd,freight,stock,stockcabinets,stockchairs,stockdesks,stocksofa,stockadd,account,role)
            db.session.add(addrole)
            db.session.commit()


    rolelist = Role.query.order_by(Role.rolename)
    catelist = Cates.query.order_by(Cates.id)
    return render_template('roles.html',session=session,nav = u"角色管理",rolelist=rolelist,catelist=catelist)

 
@app.route("/trans",methods=['POST','GET'])
@login_required
def trans():
    if request.method == 'POST':
        if request.form['submit']=="add":
            corpname = request.form['corpname']
            db.session.add(Trans(corpname))
            db.session.commit()
    translist = Trans.query.order_by(Trans.id)
    catelist = Cates.query.order_by(Cates.id)
    return render_template('transcorp.html',session=session,nav = u"物流公司",translist=translist,catelist=catelist)


@app.route("/cates",methods=['POST','GET'])
@login_required
def cates():
    if request.method == 'POST':
        if request.form['submit']=="add":
            ecate=request.form['ecate']
            categroies=request.form['categroies']
            db.session.add(Cates(ecate,categroies))
            db.session.commit()

    catelist = Cates.query.order_by(Cates.id)
    return render_template('categroies.html',session=session,nav = u"产品分类",catelist=catelist)

@app.route("/delivery",methods=['POST','GET'])
@login_required
def delivery():
    if request.method == 'POST':
        if request.form['submit']=="add":
            delivery = request.form['delivery']
            db.session.add(Delivery(delivery))
            db.session.commit()
    delilist = Delivery.query.order_by(Delivery.id)
    catelist = Cates.query.order_by(Cates.id)
    return render_template('delivery.html',session=session,nav = u"送货方式",delilist=delilist,catelist=catelist)