from flask import request, redirect, g
from . import routes
from .render import Render, Handler, debug
from .register import register_user

import bcrypt
import base64
import hashlib

def check_pw(pw=None, h=None):
    if pw and h:
        pw = base64.b64encode(hashlib.sha256(pw).digest())
        if bcrypt.checkpw(pw, h):
            return True
        else:
            debug("Login unsuccessful", type="BLOCKED")
            return False
    elif h:
        debug("Missing db entry", type="BLOCKED")
        return False
    else:
        debug("No password", type="BLOCKED")
        return False

def login_cookie(resp=None, user_id=None):
    if resp and user_id:
        resp.set_cookie('user-id', str(user_id))
        return resp
    else:
        debug("Could not set cookie")

def check_token(token=None):
    if token:
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "844750598900-4grsbbb1nnr3r50p5600h4601k0hnkm8.apps.googleusercontent.com")

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            debug("Token valid {}".format(userid), type="SUCCESS")
            return True
        except ValueError:
            # Invalid token
            debug("Invalid token", type="BUG", forceBreak=True)
            return False
    else:
        debug("No token received", type="BUG", forceBreak=True)
        return False

@routes.route('/login-google', methods=['POST'])
def login_google():
    data = request.form
    username = data['name'].encode("utf-8")
    token = data['token'].encode("utf-8")

    cur = g.sqlite_db.cursor()

    cur.execute("""
    SELECT * FROM users
        WHERE lower(username)='{}';
    """.format(username.lower())
    )

    user = cur.fetchone()
    debug(user, type="INFO")

    if user and check_token(token):
        debug("User exists {}".format(user), type="INFO")
        user_id = user[0]
        user_username = user[1]
        user_type = user[2]

        resp = redirect("/redirect?page=/")
        resp = login_cookie(resp=resp, user_id=user_id)
        return resp
    elif check_token(token):
        user_type = 1
        user = register_user(username=username, password=None, vpassword=None,
                            user_type=user_type, token=token)

        if user:
            debug("User registered {}".format(user), type="SUCCESS")
            resp = redirect("/redirect?page=/")
            resp = login_cookie(resp=resp, user_id=user[0])
            return resp
        else:
            debug("No User post-register", type="BUG", forceBreak=True)
            return False
    else:
        debug("Token invalid", type="BLOCKED", forceBreak=True)
        return False

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
        if user:
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
        else:
            message = "Incorect username/password"
            return Render.html("login.html", 403, message=message)
