
import os, sys, logging

# third-party imports
from flask import Flask, render_template, request, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

## Throws error if placed above db initialization
from models import *

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate= Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)
    
    return app
