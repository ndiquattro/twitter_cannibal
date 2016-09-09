from flask import Flask

# Initiate Flask
app = Flask(__name__,
            instance_relative_config=True,
            static_folder="./static",
            static_url_path="/static")
# app.config.from_object('config')
app.config.from_pyfile('config.py')

# Connect to database
# db = SQLAlchemy(app)

# Import Blueprints
from views.splash import splash

# Blueprints
app.register_blueprint(splash)

# Final Import
# from app.models import gbookdb

