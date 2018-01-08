#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.insert(0, '/opt/POS/')
from app import app as application
reload(sys)
sys.setdefaultencoding("utf8")


if __name__ == "__main__":
    application.run(debug=True)
    