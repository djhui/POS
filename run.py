#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.insert(0, '/opt/POS/')
from app import app as YFapp

if __name__ == "__main__":
    YFapp.run()
    