from flask import Blueprint, render_template

# Register blueprint
splash = Blueprint('splash', __name__)


@splash.route('/')
def index():
    return render_template("splash/index.html")
