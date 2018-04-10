from . import routes
from .render import Render

@routes.route('/500')
def server_error():
    return Render.html('500.html')
