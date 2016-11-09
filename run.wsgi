#!/usr/bin/python
# -*- coding:utf-8 -*-
from app import app
#from flask_debug import Debug
application=app
#Debug(app)
import sys
import sys
sys.path.insert(0, '/opt/POS/')


if __name__ == "__main__":
    if len(sys.argv)>1:
        try:
            int(sys.argv[1])
            port = int(sys.argv[1])
        except:pass
    else:
        port = 5000
    app.run(host="0.0.0.0",port=port, debug=True)
    