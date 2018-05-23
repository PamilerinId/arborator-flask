from flask import render_template
from flask_login import login_required
from app import requires_access_level
from . import home
from ..models import *


@home.route('/')
def home_page():
    """
    Home Handler
    """
    projects = Project.query.all()
    return render_template('home/index.html', projects=projects)

@home.route('/admin')
@login_required
@requires_access_level(ACCESS['admin'])
def admin_dash():      
    return render_template('home/admin.html')
    
@home.route('/q')
def q_test():
    """
    Quickie Handler
    q.cgi convert
    """
    return render_template('home/quickie.html')
