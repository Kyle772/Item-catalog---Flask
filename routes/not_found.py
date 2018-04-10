from . import routes
from .render import Render

@routes.route('/404')
def page_not_found():
    return Render.html('404.html')
