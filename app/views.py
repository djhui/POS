from flask import * 
from app import app,lm
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User
from hashlib import sha512
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',methods=['POST','GET']), 404

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
    print g.user
    user = current_user
    return render_template('main.html',user=user)

@app.route("/sales",methods=['POST','GET'])
@login_required
def sales():
    return render_template('sales.html',session=session)

@app.route("/sales/detail",methods=['POST','GET'])
@login_required
def salesdetail():
    return render_template('sales_detail.html',session=session)

@app.route("/sales/add",methods=['POST','GET'])
@login_required
def salesadd():
    return render_template('sales.html',session=session)

@app.route("/users",methods=['POST','GET'])
@login_required
def users():
    return render_template('users.html',session=session)

@app.route("/freight",methods=['POST','GET'])
@login_required
def freight():
    return render_template('freight.html',session=session)

@app.route("/stocks",methods=['POST','GET'])
@login_required
def stocks():
    return render_template('stocks.html',session=session)

@app.route("/stocks/cabinets",methods=['POST','GET'])
@login_required
def stockscabinets():
    return render_template('stocks.html',session=session)

@app.route("/stocks/chairs",methods=['POST','GET'])
@login_required
def stockschairs():
    return render_template('stocks.html',session=session)

@app.route("/stocks/desks",methods=['POST','GET'])
@login_required
def stocksdesks():
    return render_template('stocks.html',session=session)

@app.route("/stocks/sofa",methods=['POST','GET'])
@login_required
def stockssofa():
    return render_template('stocks.html',session=session)

@app.route("/stocks/add",methods=['POST','GET'])
@login_required
def stocksadd():
    return render_template('stocks.html',session=session)

@app.route("/base",methods=['POST','GET'])
@login_required
def base():
    return render_template('base.html',session=session)

 
