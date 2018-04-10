from flask import Blueprint
routes = Blueprint('routes', __name__)

from .index import *
from .login import *
from .logout import *
from .register import *
from .items import *
from .server_error import *
from .not_found import *
from .redirect import *
