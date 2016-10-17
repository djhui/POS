#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import * 
from app import app,lm
from flask_login import login_user, logout_user, current_user, login_required
from models import User,Role,db,Sales,Stock
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
    return render_template('main.html',user=user)

@app.route("/sales",methods=['POST','GET'])
@login_required
def sales():
    return render_template('sales.html',session=session,nav = u"销售总览")

@app.route("/sales/detail",methods=['POST','GET'])
@login_required
def salesdetail():
    saleslist = Sales.query.order_by(Sales.id)
    return render_template('sales_detail.html',session=session,nav = u"销售详情",saleslist=saleslist)

@app.route("/sales/add",methods=['POST','GET'])
@login_required
def salesadd():
    return render_template('salesadd.html',session=session,nav = u"添加")

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
    return render_template('users.html',session=session,nav = u"用户管理",userlist=userlist,rolelist=rolelist)

@app.route("/freight",methods=['POST','GET'])
@login_required
def freight():
    return render_template('freight.html',session=session,nav = u"运费估算")

@app.route("/stocks",methods=['POST','GET'])
@login_required
def stocks():
    stocklist = Stock.query.order_by(Stock.id)
    return render_template('stocks.html',session=session,nav = u"库存总览",stocklist=stocklist)

@app.route("/stocks/cabinets",methods=['POST','GET'])
@login_required
def stockscabinets():
    return render_template('stocks.html',session=session,nav = u"库存->柜/箱")

@app.route("/stocks/chairs",methods=['POST','GET'])
@login_required
def stockschairs():
    return render_template('stocks.html',session=session,nav = u"库存->椅/凳")

@app.route("/stocks/desks",methods=['POST','GET'])
@login_required
def stocksdesks():
    return render_template('stocks.html',session=session,nav = u"库存->桌/几")

@app.route("/stocks/sofa",methods=['POST','GET'])
@login_required
def stockssofa():
    return render_template('stocks.html',session=session,nav = u"库存->沙发")

@app.route("/stocks/add",methods=['POST','GET'])
@login_required
def stocksadd():
    return render_template('stocksadd.html',session=session,nav = u"库存->新增")

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
    return render_template('roles.html',session=session,nav = u"角色管理",rolelist=rolelist)

 
