from flask import Blueprint, render_template
from flask_login import login_required, current_user

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/home')
@login_required
def home():
    return render_template('home.html', username=current_user.username)
