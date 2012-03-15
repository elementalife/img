#!/usr/bin/env python2
# coding: utf-8
from config.url import urls
import sys, os 

abspath = os.path.dirname(__file__) 
sys.path.append(abspath) 
os.chdir(abspath) 

import web

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
else:
	application = app.wsgifunc()
