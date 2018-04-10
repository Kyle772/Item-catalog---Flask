from flask import request, redirect

from . import routes
from .render import Render
from .render import Handler

def clear_cookie(resp=None):
    if resp:
        resp.set_cookie('user-id', '', expires=0)
        return resp
    else:
        return False

@routes.route('/logout', methods=['GET'])
def logout():
    user_id = request.cookies.get("user-id")
    if user_id == None:
        return redirect("/")
    else:
        resp = redirect("/redirect?page=/")
        resp = clear_cookie(resp=resp)
        return resp
