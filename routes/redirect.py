from flask import render_template
from . import routes

@routes.route('/redirect')
def redirect():
    return render_template('redirect.html')