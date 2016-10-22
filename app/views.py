#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import * 
from app import app,lm
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from tools import *
from hashlib import sha512,md5
import os
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',methods=['POST','GET'],error=u"文件未找到"), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('error.html',methods=['POST','GET'],error=u"无权限"), 403

@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html',methods=['POST','GET'],error=u"内部服务器出错了"), 500

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

@app.route("/salesorder",methods=['POST','GET'])
@login_required
def salesorder():
    if request.method == 'POST':
        if request.form['submit']=="add":
            productid = request.form['productid']
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
            addsales = Sales(productid, orderdate, wangwang, cdeliverydate, type,color,number,address,transportation,Inprice,price,advprice,CSE,deliverydate, trancorp, Tnumber, Aprice,Recashes,Commission, memo)
            db.session.add(addsales)
            if request.form['submit']=="update":pass
            if request.form['submit']=="delete":pass
        db.session.commit()
    nickname=User.query.order_by(User.username)
    delilist = Delivery.query.order_by(Delivery.id)
    translist = Trans.query.order_by(Trans.id)
    prolist = Products.query.order_by(Products.id)
    return render_template('salesorder.html',session=session,nav = u"添加",nickname=nickname,delilist=delilist,catelist=g.catelist,translist=translist,prolist=prolist)

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
        if request.form['submit']=="delete":
            db.session.delete(newuser)
            log = u"删除用户:%s" % (newuser.username)
        db.session.add(Logs(log,u"用户管理",session['nickname'])) 
        db.session.commit()
        
    userlist = User.query.order_by(User.username)
    rolelist = Role.query.order_by(Role.rolename)
    return render_template('users.html',session=session,nav = u"用户管理",userlist=userlist,rolelist=rolelist,catelist=g.catelist)

@app.route("/freight",methods=['POST','GET'])
@login_required
def freight():
    translist = Trans.query.order_by(Trans.id)
    delilist = Delivery.query.order_by(Delivery.id)
    return render_template('freight.html',session=session,nav = u"运费估算",catelist=g.catelist,delilist=delilist,translist =translist)

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


@app.route("/purchase",methods=['POST','GET'])
@login_required
def purchase():
    if request.method == 'POST':
        if request.form['submit']=="add":
            productid = request.form['productid']
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
            addstock = Stock(productid, products,categroies,code,specification,color,exstock,whstock,fastock,pkgsize,pgkbulk,memo)
            db.session.add(addstock)
            db.session.commit()
            stocklist = Stock.query.order_by(Stock.id)
            return render_template('stocks.html',session=session,nav = u"库存总览",stocklist=stocklist,catelist=g.catelist)
            log = u"添加库存:ID->%s,产品名->%s,规格->%s,编码->%s,颜色->%s,展厅数量->%s,仓库数量->%s,工厂数量->%s" % productid, products,categroies,code,color,exstock,whstock,fastock
        if request.form['submit']=="update":pass
        if request.form['submit']=="delete":pass
        db.session.add(Logs(log,u"采购产品",session['nickname'])) 
    prolist = Products.query.order_by(Products.id)
    return render_template('purchase.html',session=session,nav = u"库存->新增",catelist=g.catelist, prolist = prolist)
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
        except:rolename="noname"
        try:sales = to_bool(request.form['sales'])
        except:sales=0
        try:salesdetail = to_bool(request.form['salesdetail'])
        except:salesdetail=0
        try:salesadd = to_bool(request.form['salesadd'])
        except:salesadd=0
        try:freight = to_bool(request.form['freight'])
        except:freight=0
        try:stock = to_bool(request.form['stock'])
        except:stock=0
        try:stockcabinets = to_bool(request.form['stockcabinets'])
        except:stockcabinets=0
        try:stockchairs = to_bool(request.form['stockchairs'])
        except:stockchairs=0
        try:stockdesks = to_bool(request.form['stockdesks'])
        except:stockdesks=0
        try:stocksofa = to_bool(request.form['stocksofa'])
        except:stocksofa=0
        try:stockadd = to_bool(request.form['stockadd'])
        except:stockadd=0
        try:account = to_bool(request.form['account'])
        except:account=0
        try:role = to_bool(request.form['role'])
        except:role=0
        print type(role)
        if request.form['submit']=="add":
            db.session.add(Role(rolename,sales,salesdetail,salesadd,freight,stock,stockcabinets,stockchairs,stockdesks,stocksofa,stockadd,account,role))
            log = u"添加角色:%s" % rolename
        if request.form['submit']=="update":
            newrole.sales,newrole.salesdetail,newrole.salesadd,newrole.freight,newrole.stock,newrole.stockcabinets,newrole.stockchairs,newrole.stockdesks,newrole.stocksofa,newrole.stockadd,newrole.account,newrole.role = sales,salesdetail,salesadd,freight,stock,stockcabinets,stockchairs,stockdesks,stocksofa,stockadd,account,role
            log = u"更改角色:%s" % newrole.rolename
        if request.form['submit']=="delete":
            db.session.delete(newrole)
            log = u"删除角色:%s" % newrole.rolename
        db.session.add(Logs(log,u"角色管理",session['nickname'])) 
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
            log=u"添加物流公司[%s]" % (corpname)
        if request.form['submit']=="update":
            newcorp.corpname = corpname
            log=u"更新物流公司[%s]为[%s]" % (newcorp.corpname,corpname)
        if request.form['submit']=="delete":
            db.session.delete(newcorp)
            log=u"删除物流公司%s" % newcorp.corpname
        db.session.add(Logs(log,u"物流公司",session['nickname'])) 
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
            log = u"添加产品类别[%s-%s]" % ecate,categroies
        if request.form['submit']=="update":
            newcate.ecate = ecate
            newcate.categroies = categroies
            log = u"更新产品类别[%s->%s][%s->%s]" % (newcate.ecate,ecate,newcate.categroies,categroies)
        if request.form['submit']=="delete":
            log = u"删除产品类别[%s-%s]" % (newcate.ecate,newcate.categroies)
            db.session.delete(newcate)
        db.session.add(Logs(log,u"产品类别",session['nickname'])) 
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
            log = u"添加送货方式[%s]" % delivery
        if request.form['submit']=="update":
            newdeli.delivery = delivery
            log = u"更新送货方式[%s->%s]" % (newdeli.delivery,delivery)
        if request.form['submit']=="delete":
            db.session.delete(newdeli)
            log = u"删除送货方式[%s]" % newdeli.delivery
        db.session.add(Logs(log,u"送货方式",session['nickname'])) 
        db.session.commit()
    delilist = Delivery.query.order_by(Delivery.id)
    return render_template('delivery.html',session=session,nav = u"送货方式",delilist=delilist,catelist=g.catelist)
#----------------------------------------------------------------------
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['files[]']
        ext = f.filename.split(".")[-1]
        filename = md5(f.filename).hexdigest() + "." + ext
        minetype = f.content_type
        f.save(os.getcwd()+'/app/static/upload/' + filename) 
        return json.dumps({"files": [{"name": filename, "minetype": minetype}]})
        log = u"上传文件%s" %filename
        db.session.add(Logs(log,u"上传文件",session['nickname'])) 
        db.session.commit()

@app.route("/log",methods=['POST','GET'])
@login_required
def log():
    loglist = Logs.query.order_by(Logs.id)
    return render_template('log.html',session=session,nav = u"操作日志",catelist=g.catelist,loglist=loglist)

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
        try:pkgsize = request.form['pkgsize']
        except:pass
        try:pgkbulk = request.form['pgkbulk']
        except:pass
        try:categroies = request.form['categroies']
        except:pass
        try:memo = request.form['memo']
        except:pass
        if request.form['submit']=="update":
            if request.form['picture']:
                newpro.picture=picture
            newpro.products, newpro.code, newpro.specification, newpro.pkgsize, newpro.pgkbulk, newpro.categroies,newpro.memo  = products, code, specification, pkgsize, pgkbulk, categroies, memo
            log = u"更改产品:名称->%s,规格->%s,编号->%s,包装尺寸->%s,包装体积->%s,类别->%s,备注->%s" % (products,categroies,code,specification,pkgsize,pgkbulk,memo)
        if request.form['submit']=="delete":
            db.session.delete(newpro)
            log = u"删除产品:名称->%s,规格->%s,编号->%s,包装尺寸->%s,包装体积->%s,类别->%s,备注->%s" % (newpro.products,newpro.categroies,newpro.code,newpro.specification,newpro.pkgsize,newpro.pgkbulk,newpro.memo)
        db.session.add(Logs(log,u"产品管理",session['nickname']))
        db.session.commit()
    prolist = Products.query.order_by(Products.id)
    return render_template('products.html',session=session,nav = u"全部产品",catelist=g.catelist,prolist=prolist)

@app.route("/productsadd",methods=['POST','GET'])
@login_required
def productsadd():
    if request.method == 'POST':
    
        try:picture = request.form['picture']
        except:pass
        try:products = request.form['products']
        except:pass
        try:code = request.form['code']
        except:pass
        try:specification = request.form['specification']
        except:pass
        try:pkgsize = request.form['pkgsize']
        except:pass
        try:pgkbulk = request.form['pgkbulk']
        except:pass
        try:categroies = request.form['categroies']
        except:pass
        try:memo= request.form['memo']
        except:pass
        if request.form['submit']=="add":
            
            db.session.add(Products(picture, products,categroies,code,specification,pkgsize,pgkbulk,memo))
            log = u"新建产品:名称->%s,规格->%s,编号->%s,包装尺寸->%s,包装体积->%s,类别->%s,备注->%s" % (products,categroies,code,specification,pkgsize,pgkbulk,memo)
        db.session.add(Logs(log,u"新建产品",session['nickname']))
        db.session.commit()
    return render_template('productadd.html',session=session,nav = u"添加产品",catelist=g.catelist)