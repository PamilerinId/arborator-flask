from flask import Blueprint

home = Blueprint('projects', __name__)

from . import views