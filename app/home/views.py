from flask import render_template
from . import home
from ..models import *


@home.route('/')
def home_page():
    """
    Home Handler
    """
    projects = Project.query.all()
    return render_template('home/index.html', projects=projects)


@home.route('/q')
def q_test():
    """
    Quickie Handler
    q.cgi convert
    """
    return render_template('home/quickie.html')
