from flask import render_template
from . import routes

@routes.route('/logout')
def logout():
    return render_template('logout.html')