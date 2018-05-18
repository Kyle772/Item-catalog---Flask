from flask import Blueprint
routes = Blueprint('routes', __name__)
GoogleClient_ID = "844750598900-4grsbbb1nnr3r50p5600h4601k0hnkm8.apps.googleusercontent.com"
GoogleClient_Secret = "gb2gqohhV15uyIoHG3mWM5rz"

from .index import *
from .login import *
from .logout import *
from .register import *
from .items import *
from .server_error import *
from .not_found import *
from .redirect import *
