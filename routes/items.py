from . import routes
from .render import Render

@routes.route('/items')
def items():
    return Render.html('items.html')
