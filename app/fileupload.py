#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
from app import app, lm
from sqlalchemy.sql import func
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from tools import *
from hashlib import sha512, md5
import os, json
from datetime import datetime
from dateutil.relativedelta import relativedelta
@app.route("/fileupload",methods=['POST','GET'])
@login_required
def fileupload():
    if request.method == 'POST':
        try:
            id = request.form['id']
            files = fileupload.query.get(id)
        except:pass
        try:
            filename = request.form['filename']
        except:pass
        try:uploadtime = request.form['uploadtime']
        except:pass
        if request.form['submit']=="add":
            if not FileUpload.query.filter_by(filename=filename).first():
                db.session.add(FileUpload(filename))
        #db.session.add(Logs(log,u"上传文件",session['nickname']))
        db.session.commit()
    filelist = FileUpload.query.order_by(FileUpload.id)
    return render_template('fileupload.html',session=session,nav = u"文件上传",catelist=g.catelist,filelist=filelist)