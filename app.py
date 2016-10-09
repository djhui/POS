from flask import * 

import sys
app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'


@app.route("/",methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin': 
            error= "sorry"
        else:
            session['name'] = request.form['username']

            return redirect(url_for('main'))
    return render_template('index.html',error=error)
 
@app.route("/exit",methods=['POST','GET'])
def exit():
    session['name']=None
    return redirect(url_for('login'))

@app.route("/main",methods=['POST','GET'])

def main():
    return render_template('main.html',session=session)

@app.route("/sales",methods=['POST','GET'])
def sales():
    return render_template('sales.html',session=session)

@app.route("/sales/detail",methods=['POST','GET'])
def salesdetail():
    return render_template('sales_detail.html',session=session)

@app.route("/sales/add",methods=['POST','GET'])
def salesadd():
    return render_template('sales.html',session=session)

@app.route("/users",methods=['POST','GET'])
def users():
    return render_template('users.html',session=session)

@app.route("/freight",methods=['POST','GET'])
def freight():
    return render_template('freight.html',session=session)

@app.route("/stocks",methods=['POST','GET'])
def stocks():
    return render_template('stocks.html',session=session)

@app.route("/stocks/cabinets",methods=['POST','GET'])
def stockscabinets():
    return render_template('stocks.html',session=session)

@app.route("/stocks/chairs",methods=['POST','GET'])
def stockschairs():
    return render_template('stocks.html',session=session)

@app.route("/stocks/desks",methods=['POST','GET'])
def stocksdesks():
    return render_template('stocks.html',session=session)

@app.route("/stocks/sofa",methods=['POST','GET'])
def stockssofa():
    return render_template('stocks.html',session=session)

@app.route("/stocks/add",methods=['POST','GET'])
def stocksadd():
    return render_template('stocks.html',session=session)

@app.route("/base",methods=['POST','GET'])
def base():
    return render_template('base.html',session=session)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',methods=['POST','GET']), 404
 
if __name__ == "__main__":
    if len(sys.argv)>1:
        try:
            int(sys.argv[1])
            port = int(sys.argv[1])
        except:
            port = 5000
    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=True)