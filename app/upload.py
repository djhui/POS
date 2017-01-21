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