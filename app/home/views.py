from flask import render_template
from . import home



@home.route('/')
def home_page():
    """
    Home Handler
    """
    return render_template('home/index.html')
    
@home.route('/q')
def q_test():
    """
    Quickie Handler
    q.cgi convert
    """
    return render_template('home/quickie.html')
