from flask import request, redirect, g
from . import routes
from .render import Render, Handler

import bcrypt
import base64
import hashlib

def check_pw(pw=None, h=None):
    if pw and h:
        pw = base64.b64encode(hashlib.sha256(pw).digest())
        if bcrypt.checkpw(pw, h):
            return True
        else:
            print("Login unsuccessful")
            return False
    else:
        print("Missing password or db entry")
        return False

def login_cookie(resp=None, user_id=None):
    if resp and user_id:
        resp.set_cookie('user-id', str(user_id))
        return resp
    else:
        print("Could not set cookie")

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        user_id = Handler.current_user_id()
        if user_id:
            return redirect('/')
        else:
            return Render.html('login.html')
    elif request.method == 'POST':
        data = request.form
        username = data['user'].encode("utf-8")
        pw = data['pass'].encode("utf-8")

        cur = g.sqlite_db.cursor()

        cur.execute("""
        SELECT * FROM users
            WHERE lower(username)='{}';
        """.format(username.lower())
        )

        user = cur.fetchone()
        user_id = user[0]
        user_username = user[1]
        user_hash = user[2]

        if check_pw(pw=pw, h=user_hash):
            resp = redirect("/redirect?page=/")
            resp = login_cookie(resp=resp, user_id=user_id)
            return resp
        else:
            message = "Incorect username/password"
            return Render.html("login.html", 403, message=message)
