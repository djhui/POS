#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
from app import app, lm
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', methods=['POST', 'GET'], error=u"文件未找到"), 404
@app.errorhandler(403)
def page_not_found(e):
    return render_template('error.html', methods=['POST', 'GET'], error=u"无权限"), 403
@app.errorhandler(400)
def page_not_found(e):
    return render_template('error.html', methods=['POST', 'GET'], error=u"服务器出错了"), 400
@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', methods=['POST', 'GET'], error=u"内部服务器出错了"), 500