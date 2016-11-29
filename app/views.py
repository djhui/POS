#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import * 
from app import app,lm
from sqlalchemy.sql import func
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from tools import *
from hashlib import sha512,md5
import os,json
from datetime import datetime
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html',methods=['POST','GET'],error=u"文件未找到"), 404
#@app.errorhandler(403)
#def page_not_found(e):
#    return render_template('error.html',methods=['POST','GET'],error=u"无权限"), 403
#@app.errorhandler(400)
#def page_not_found(e):
#    return render_template('error.html',methods=['POST','GET'],error=u"服务器出错了"), 400
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

#----------------------------------------------------------------------
@app.route("/main",methods=['POST','GET'])
@login_required
def main():
    return render_template('main.html',user=g.user,catelist=g.catelist)
#----------------------------------------------------------------------
@app.route("/sales",methods=['POST','GET'])
@login_required
def sales():
    if request.method == 'POST':
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        CSE = request.form['CSE']
        SalesSum = []
        if CSE == "all":
            CSE = u"全店"
            sumre = db.session.query(func.sum(Sales.price),func.sum(Sales.advprice),func.sum(Sales.Recashes)).filter("orderdate<=:enddate","orderdate>=:startdate","offset=:offset").params(startdate=startdate,enddate=enddate,offset=0).first()
            transfee = db.session.query(func.sum(Sales.Aprice)).filter("orderdate<=:enddate","orderdate>=:startdate","transportation not like :transportation","offset=:offset").params(startdate=startdate,enddate=enddate,transportation=u"%到付%",offset=0).first()
        else:
            sumre = db.session.query(func.sum(Sales.price),func.sum(Sales.advprice),func.sum(Sales.Recashes)).filter("CSE=:CSE","orderdate<=:enddate","orderdate>=:startdate","offset=:offset").params(CSE=CSE,startdate=startdate,enddate=enddate,offset=0).first()
            transfee = db.session.query(func.sum(Sales.Aprice)).filter("CSE=:CSE","orderdate<=:enddate","orderdate>=:startdate","transportation not like :transportation","offset=:offset").params(CSE=CSE,startdate=startdate,enddate=enddate,transportation=u"%到付%",offset=0).first()
        price = sumre[0] + sumre[1]
        result = {'id':'id','employee':CSE,'price':"%.2f" % price,'Aprice':"%.2f" %transfee[0] ,'Recashes':"%.2f" % sumre[2]}
        SalesSum.append(result)
        return json.dumps({'msg':SalesSum})
    nickname=User.query.order_by(User.username)
    return render_template('sales.html',session=session,nav = u"销售总览",catelist=g.catelist,nickname=nickname)
#---------------------------------------------------------------------------------------
@app.route("/sales/detail",methods=['POST','GET'])
@login_required
def salesdetail():
    if request.method == 'POST':
        id = request.form['id']
        newsales = Sales.query.filter_by(id=id).first()

        if request.form['submit']=="update":
            transportation = request.form['transportation']
            try:Inprice = float(request.form['Inprice'])
            except:Inprice=None
            try:Aprice = float(request.form['Aprice'])
            except:Aprice=None
            try:Recashes = float(request.form['Recashes'])
            except:Recashes=None
            Commission = request.form['Commission']
            if Commission == "None":Commission=None
            deliverydate = request.form['deliverydate']
            trancorp = request.form['trancorp']
            Tnumber = request.form['Tnumber']
            memo = request.form['memo']
            newsales.transportation,newsales.Inprice,newsales.deliverydate,newsales.trancorp,newsales.Tnumber,newsales.Aprice,newsales.Recashes,newsales.Commission,newsales.memo = transportation, Inprice, deliverydate, trancorp, Tnumber, Aprice, Recashes, Commission, memo
            log = u"更新订单:%s" % id
        if request.form['submit']=="delete":
            log = memo = u"冲销订单%s" % newsales.id
            newsales.offset=1
            newsales.memo = memo
            for i in range(0, 10):
                if eval("newsales.productid%s" %i):
                    proinfo = Products.query.filter_by(id=eval("newsales.productid%s" %i)).first()
                    if eval("newsales.warehouse%s" %i) == "exstock" : proinfo.exstock = proinfo.exstock + eval("newsales.number%s" %i)
                    if eval("newsales.warehouse%s" %i) == "whstock" : proinfo.whstock = proinfo.whstock + eval("newsales.number%s" %i)
                    if eval("newsales.warehouse%s" %i) == "fastock" : proinfo.fastock = proinfo.fastock + eval("newsales.number%s" %i)
            db.session.add(Sales(newsales.picture,newsales.orderdate,newsales.wangwang,newsales.cdeliverydate,newsales.type1,newsales.address,newsales.transportation,newsales.Inprice,newsales.price,newsales.advprice,newsales.CSE,newsales.deliverydate,newsales.trancorp,newsales.Tnumber,newsales.Aprice,newsales.Recashes,newsales.Commission,newsales.offset,newsales.memo,newsales.productid0,newsales.warehouse0,newsales.code0,newsales.number0,newsales.productid1,newsales.warehouse1,newsales.code1,newsales.number1,newsales.productid2,newsales.warehouse2,newsales.code2,newsales.number2,newsales.productid3,newsales.warehouse3,newsales.code3,newsales.number3,newsales.productid4,newsales.warehouse4,newsales.code4,newsales.number4,newsales.productid5,newsales.warehouse5,newsales.code5,newsales.number5,newsales.productid6,newsales.warehouse6,newsales.code6,newsales.number6,newsales.productid7,newsales.warehouse7,newsales.code7,newsales.number7,newsales.productid8,newsales.warehouse8,newsales.code8,newsales.number8,newsales.productid9,newsales.warehouse9,newsales.code9,newsales.number9,newsales.color0))

            log = u"冲销订单:%s" % newsales.id
            db.session.add(Logs(log,u"销售管理",session['nickname'])) 
        if request.form['submit']=="getpro":
            allpro = []
            names = locals()
            for i in range(0, 10):
                if eval("newsales.productid%s" %i):
                    proinfo = Products.query.filter_by(id=eval("newsales.productid%s" %i)).first()
                    if eval("newsales.warehouse%s" %i) == u'exstock': warehouse = u"展厅"
                    if eval("newsales.warehouse%s" %i) == u'whstock': warehouse = u"仓库"
                    if eval("newsales.warehouse%s" %i) == u'fastock': warehouse = u"工厂"
                    result = {'id':eval("newsales.productid%s" %i),'picture':'<img src="../static/upload/'+proinfo.picture+'" width="200" />','products':proinfo.products,'specification':proinfo.specification,'color':proinfo.color,'warehouse':warehouse,'number':eval("newsales.number%s" %i)}
                    allpro.append(result)
                    print eval("newsales.productid%s" %i)
                #print json.dumps(Cals)
            
            return json.dumps({'msg':allpro})
        db.session.commit()
    saleslist = db.session.query(Sales.id,Sales.picture,Sales.orderdate,Sales.wangwang,Sales.cdeliverydate,Sales.type1,Sales.color0,Sales.number0,Sales.address,Sales.transportation,Sales.Inprice,Sales.price,Sales.advprice,Sales.CSE,Sales.deliverydate,Sales.trancorp,Sales.Tnumber,Sales.Aprice,Sales.Recashes,Sales.Commission,Sales.memo,Sales.offset,Sales.productid1).all()
    prolist = Products.query.order_by(Products.id)
    delilist = Delivery.query.order_by(Delivery.id)
    translist = Trans.query.order_by(Trans.id)
    return render_template('sales_detail.html',session=session,nav = u"销售详情",saleslist=saleslist,delilist=delilist,catelist=g.catelist,translist=translist,prolist=prolist)
#--------------------------------------------------------------------------------------------------------------------
@app.route("/salesorder",methods=['POST','GET'])
@login_required
def salesorder():
    names = locals()
    if request.method == 'POST':
        for i in xrange(0, 10):
            try:
                names['productid%s' % i] = request.form['productid%s' % i]
                names['number%s' % i] = int(request.form['number%s' % i])
                names['warehouse%s' % i] = request.form['warehouse%s' % i]
                names['code%s' % i] = request.form['code%s' % i]
                names['color%s' % i] = request.form['color%s' % i]
                print names['productid%s' % i]
                newpro = Products.query.filter_by(id=names['productid0']).first()
                picture = newpro.picture
            except:
                names['productid%s' % i] = names['number%s' % i] = names['warehouse%s' % i] = names['code%s' % i] = names['color%s' % i] = None
            if names['warehouse%s' % i] == "exstock" : newpro.exstock = newpro.exstock - names['number%s' % i]
            if names['warehouse%s' % i] == "whstock" : newpro.whstock = newpro.whstock - names['number%s' % i]
            if names['warehouse%s' % i] == "fastock" : newpro.fastock = newpro.fastock - names['number%s' % i]
        orderdate = request.form['orderdate']
        wangwang = request.form['wangwang']
        cdeliverydate = request.form['cdeliverydate']
        type1 = request.form['specification0']
        color = request.form['color0']
        warehouse = number = transportation = Inprice = deliverydate = trancorp = Tnumber = Aprice = Recashes = Commission = None 

        address = request.form['address']
        price = float(request.form['price'])
        advprice = float(request.form['advprice'])
        CSE = request.form['CSE']
        offset = 0
        try:memo = request.form['memo']
        except:memo="no comments"
        if request.form['submit']=="add":
            addsales = Sales(picture,orderdate, wangwang, cdeliverydate, type1,address,transportation,Inprice,price,advprice,CSE,deliverydate, trancorp, Tnumber, Aprice,Recashes,Commission,offset,memo,names['productid0'], names['warehouse0'], names['code0'], names['number0'], names['productid1'], names['warehouse1'], names['code1'], names['number1'], names['productid2'], names['warehouse2'], names['code2'], names['number2'],names['productid3'], names['warehouse3'], names['code3'], names['number3'], names['productid4'], names['warehouse4'], names['code4'], names['number4'], names['productid5'], names['warehouse5'], names['code5'], names['number5'], names['productid6'], names['warehouse6'], names['code6'], names['number6'], names['productid7'], names['warehouse7'], names['code7'], names['number7'], names['productid8'], names['warehouse8'], names['code8'], names['number8'], names['productid9'], names['warehouse9'], names['code9'], names['number9'],color)
            db.session.add(addsales)
            log = u"添加订单:产品ID->%s,下单日期->%s,旺旺->%s,客户要求发货日期->%s,规格->%s,颜色->%s,发货仓库->%s,下单数量->%s,发货地址->%s,物流送货方式->%s,保费->%s,商品价格->%s,预收运费->%s,客服->%s,实际发货日期->%s,物流公司->%s,物流单号->%s,,实际运费->%s,返现->%s,提成结算日期->%s,备注->%s" % (names['productid0'],orderdate,wangwang,cdeliverydate,type1,names['color0'],names['warehouse0'],names['number0'],address,transportation,Inprice,price,advprice,CSE,deliverydate,trancorp,Tnumber,Aprice,Recashes,Commission,memo)
        db.session.add(Logs(log,u"销售订单",session['nickname'])) 
        db.session.commit()
    nickname=User.query.order_by(User.username)
    prolist = Products.query.order_by(Products.id)
    return render_template('salesorder.html',session=session,nav = u"添加",nickname=nickname,catelist=g.catelist,prolist=prolist)
#----------------------------------------------------------------------
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
        if request.form['submit']=="uppswd":
            newuser.password=password
            log = u"%s更改了密码" % (newuser.username)
        if request.form['submit']=="delete":
            db.session.delete(newuser)
            log = u"删除用户:%s" % (newuser.username)
        db.session.add(Logs(log,u"用户管理",session['nickname'])) 
        db.session.commit()
        
    userlist = User.query.order_by(User.username)
    rolelist = Role.query.order_by(Role.rolename)
    return render_template('users.html',session=session,nav = u"用户管理",userlist=userlist,rolelist=rolelist,catelist=g.catelist)
#----------------------------------------------------------------------
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
@app.route("/purlist",methods=['POST','GET'])
@login_required
def purlist():
    if request.method == 'POST':
        try:
            id = request.form['id']
            newstock = Stock.query.get(id)
            newpro = Products.query.filter_by(id=newstock.productid).first()
        except:pass
        if request.form['submit']=="delete":
            newstock.offset=1
            memo=u"冲销订单%s" % id
            db.session.add(Stock(newstock.productid,newstock.picture,newstock.products,newstock.code,newstock.specification,newstock.color,newstock.exstock,newstock.whstock,newstock.fastock,newstock.offset,memo))
            newpro.exstock = newpro.exstock - newstock.exstock
            newpro.whstock = newpro.whstock - newstock.whstock
            newpro.fastock = newpro.fastock - newstock.fastock
            log = memo
        db.session.add(Logs(log,u"采购产品",session['nickname'])) 
        db.session.commit()
    stocklist = Stock.query.order_by(Stock.id)
    return render_template('purlist.html',session=session,nav = u"采购订单记录",stocklist=stocklist,catelist=g.catelist)
#------------------------------------------------------------------------------------------------------------
@app.route("/purchase",methods=['POST','GET'])
@login_required
def purchase():
    if request.method == 'POST':
        if request.form['submit']=="add":
            productid = request.form['productid']
            newpro = Products.query.filter_by(id=productid).first()
            products = request.form['products']
            code = request.form['code']
            specification = request.form['specification']
            color = request.form['color']
            exstock = int(request.form['exstock'])
            whstock = int(request.form['whstock'])
            fastock = int(request.form['fastock'])
            try:memo= request.form['memo']
            except:memo="no comments"
            db.session.add(Stock(productid,newpro.picture, products,code,specification,color,exstock,whstock,fastock,0,memo))
            stocklist = Stock.query.order_by(Stock.id)
            exstock += newpro.exstock
            whstock += newpro.whstock
            fastock += newpro.fastock
            newpro.exstock,newpro.whstock,newpro.fastock=exstock,whstock,fastock
            log = u"添加库存:ID->%s,产品名->%s,颜色->%s,展厅数量->%s,仓库数量->%s,工厂数量->%s" % (productid, products,color,exstock,whstock,fastock)
            db.session.add(Logs(log,u"采购产品",session['nickname'])) 
            db.session.commit()
            stocklist = Stock.query.order_by(Stock.id)
            return render_template('purlist.html',session=session,nav = u"采购订单记录",stocklist=stocklist,catelist=g.catelist)
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
        filename = md5(str(datetime.now())).hexdigest() + "." + ext
        minetype = f.content_type
        if ext.lower() not in ['jpg','jpeg','png','bmp','gif']:
            return json.dumps({"files": [{"name": u"文件格式错误,请上传图片格式", "minetype": minetype}]})
        else:    
            #filename1 = './app/static/upload/%s' % (filename)
            filename1 = '/opt/POS/app/static/upload/%s' % (filename)
            f.save(filename1) 
            log = u"上传文件%s" %filename
            db.session.add(Logs(log,u"上传文件",session['nickname'])) 
            db.session.commit()
            return json.dumps({"files": [{"name": filename, "minetype": minetype}]})
#----------------------------------------------------------------------
@app.route("/log",methods=['POST','GET'])
@login_required
def log():
    loglist = Logs.query.order_by(Logs.id)
    return render_template('log.html',session=session,nav = u"操作日志",catelist=g.catelist,loglist=loglist)
#----------------------------------------------------------------------
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