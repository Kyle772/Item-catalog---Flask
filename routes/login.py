from flask import render_template, request
from . import routes
from . import secret

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return render_template('redirect.html')