from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initiate Flask
app = Flask(__name__, instance_relative_config=True)

# Point at config file
app.config.from_pyfile('config.py')

# Connect to database
db = SQLAlchemy(app)

# Import Blueprints
from views.splash import splash
from views.auth import auth

# Blueprints
app.register_blueprint(splash)
app.register_blueprint(auth)

# Final Import
from app import models

