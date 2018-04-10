from . import routes
from .render import Render

@routes.route('/')
def index():
    return Render.html('index.html')
