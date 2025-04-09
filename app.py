from flask import Flask, redirect, url_for
from flask_login import LoginManager
from auth import auth_blueprint
from tasks import tasks_blueprint
from flask import Flask, render_template, redirect, url_for
# If you're using the separate login.py module:
# from login import login_blueprint
from home import home_blueprint
from models import User
from config import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # or 'login.login' if using login_blueprint

# Define the user_loader callback
@login_manager.user_loader
def load_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    connection.close()
    if user:
        return User(user['id'], user['username'])
    return None

# Register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(home_blueprint)
# If using separate login module:
# app.register_blueprint(login_blueprint)
@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/')
def index():
    return redirect(url_for('about'))


if __name__ == '__main__':
    app.run(debug=True)
