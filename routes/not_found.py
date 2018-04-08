from flask import render_template
from . import routes

@routes.route('/404')
def page_not_found():
    return render_template('404.html')