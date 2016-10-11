from flask import Flask
import MySQLdb
from flask.ext.sqlalchemy import SQLAlchemy
  
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/flask'
db = SQLAlchemy(app)
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(320), unique=True)
    role = db.Column(db.String(32), nullable=False)
  
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role= role
#password = admin
inset=User(username='admin', password='c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec', role='admin')
db.session.add(inset)
db.session.commit()