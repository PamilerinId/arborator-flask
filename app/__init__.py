
import os, sys, logging
from functools import wraps

# third-party imports
from flask import Flask, render_template, request, make_response, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

login_manager = LoginManager()
# Throws error if placed above db initialization
from models import *


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('email'):
                return redirect(url_for('users.login'))
            user = User.query.filter_by(email=session['email']).first_or_404()
            if not user.allowed(access_level):
                return redirect(url_for('home.home_page', message="You do not have access to that page. Sorry!"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    login_manager.init_app(app)
    migrate= Migrate(app, db)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.choose_provider"

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .project import project as project_blueprint
    app.register_blueprint(project_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500
    
    return app
