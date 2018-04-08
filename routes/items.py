from flask import render_template
from . import routes

@routes.route('/items')
def items():
    return render_template('items.html')