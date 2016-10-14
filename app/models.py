#!/usr/bin/python
# -*- coding:utf-8 -*-
from hashlib import md5
from app import app
from app import db

ROLE_USER = 0
ROLE_ADMIN = 1



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(320), unique=True)
    nickname = db.Column(db.String(80), unique=True)
    mobile = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(32), nullable=False)

    @staticmethod
    def make_unique_nickname(username):
        pass
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

        
    def __repr__(self):
        return '<User %r>' % (self.username)    
        

        

