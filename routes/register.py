from flask import request, redirect, g
from . import routes
from .render import Render, Handler, debug

import bcrypt
import base64
import hashlib

def make_pw_hash(pw=None):
    # 256 + b64 for greater than 75 char limit
    if pw:
        pw = base64.b64encode(hashlib.sha256(pw).digest())
        h = bcrypt.hashpw(pw, bcrypt.gensalt())
        return h
    else:
        return False

def register_user(username, password, vpassword, user_type, token=None):
    # User_type is from google sign in
    if user_type == 1 and password == None:
        insert = (username, user_type, token)

        cur = g.sqlite_db.cursor()
        cur.execute("""
        SELECT * FROM users WHERE lower(username)='{}'
        """.format(username.lower())
        )
        user = cur.fetchone()
        debug(user, type="INFO")

        # If user not found
        if not user:
            debug(insert, type="PUTTING")
            cur.execute("""
            INSERT INTO users (username, user_type, token)
            VALUES {}
            RETURNING *;
            """.format(insert,)
            )

            user = cur.fetchone()
            debug(user, type="RESPONSE")

            g.sqlite_db.commit()
            return user
        # else found
        else:
            message = "Username already exists"
            debug(message, type="NA")
            return False
    # User Not from Google
    elif password == vpassword:
        password_hash = make_pw_hash(password)
        insert = (username, password_hash, user_type)

        cur = g.sqlite_db.cursor()
        cur.execute("""
        SELECT * FROM users WHERE lower(username)='{}'
        """.format(username)
        )
        user = cur.fetchone()
        debug(user)
        # If user is NOT found
        if not user:
            cur.execute("""
            INSERT INTO users (username, password_hash, user_type)
            VALUES {};
            """.format(insert,)
            )

            g.sqlite_db.commit()
            return redirect("/redirect?page=/")
        # Else user is found
        else:
            message = "Username already exists"
            return Render.html("register.html", 403, message=message)
    else:
        message = "Passwords don't match"
        return Render.html("register.html", 403, message=message)

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return Render.html('register.html')
    elif request.method == 'POST':
        data = request.form
        username = data['user'].encode("utf-8")
        password = data['pass'].encode("utf-8")
        vpassword = data['vpass'].encode("utf-8")
        user_type = 0
        return register_user(username, password, vpassword, user_type)
