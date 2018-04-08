from flask import render_template
from . import routes

@routes.route('/500')
def server_error():
    return render_template('500.html')