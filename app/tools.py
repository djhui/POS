#!/usr/bin/python
# -*- coding:utf-8 -*-
def to_bool(value):
    if str(value).lower() =="true": 
        return True
    elif str(value).lower() =="false": 
        return False
    elif type(value)==bool:
        return value
    else:return value