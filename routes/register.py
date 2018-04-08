from flask import render_template, request
from . import routes
from . import secret

@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.form
        password = data['pass']
        vpassword = data['vpass']
        username = data['user']
        
        return render_template('redirect.html')