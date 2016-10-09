from flask import * 
 
app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
@app.route("/",methods=['POST','GET'])
 
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin123': 
            session['name'] = request.form['username']
            error= "sorry"
        else:
            return redirect(url_for('index'))
    return render_template('login.html',error=error)
 
 
@app.route("/index")
def index():
    
    return render_template('index.html',session=session)

@app.route("/base")
def base():
    return render_template('base.html',session=session)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
 
if __name__ == "__main__":
    app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=True)