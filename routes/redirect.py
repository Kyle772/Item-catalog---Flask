from flask import request

from . import routes
from .render import Render

@routes.route('/redirect')
def redirect():
    if request.method == 'GET':
        page = request.args.get("page")
        return Render.html('redirect.html', page=page)
