#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
import jinja2

import json
import os
from paste import httpserver

import psycopg2 as psql

from routes import *

app = Flask(__name__)
app.register_blueprint(routes)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)
        
class Db():
    def open(dbname="flask", *args, **kwargs):
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = psql.connect("dbname=" + dbname)
        return g.sqlite_db
    
    def close():
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()
        
@app.before_request
def before_request():
    g = Db.open()

@app.teardown_appcontext
def teardown_request(exception):
    g = Db.close()
        
def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8080')
    os.system('attrib +H *.pyc /S')
    
if __name__ == '__main__':
    main()