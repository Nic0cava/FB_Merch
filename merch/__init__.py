# merch/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import session, request, redirect, url_for, flash

from dotenv import load_dotenv  # <-- Load .env file
# Load environment variables from .env
load_dotenv()


app = Flask(__name__)

# SECRET_KEY setup
app.secret_key = os.getenv('SECRET_KEY')

#####################################
###### DATABASE SETUP ###############
# PostgreSQL connection string from .env
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# Optional config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# Initialize extensions
db = SQLAlchemy(app)
Migrate(app, db)
#####################################
#####################################



from merch.core.views import core
from merch.error_pages.handlers import error_pages
from merch.categories.views import category
from merch.items.views import items
from merch.auth import auth
app.register_blueprint(items)
app.register_blueprint(category)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(auth)

# Gate all routes behind a simple shared-password session flag
@app.before_request
def require_login_for_app():
    # allowed endpoints without auth
    allowed = {
        'static',
        'auth.login',
    }
    # if endpoint is None (e.g., 404) or explicitly allowed, let it through
    if request.endpoint in allowed:
        return None

    if session.get('authed'):
        return None

    # redirect to login with next param
    if request.endpoint != 'auth.login':
        return redirect(url_for('auth.login', next=request.url))
    return None

# Seed initial password from env var if present and not yet configured
try:
    from merch.models import AppAuth
    with app.app_context():
        # only seed on empty table and when env var is provided
        initial_pw = os.getenv('APP_SHARED_PASSWORD')
        if initial_pw:
            rec = AppAuth.query.get(1)
            if rec is None:
                AppAuth.set_password(initial_pw)
except Exception:
    # Avoid import/DB errors during migrations or uninitialized DB
    pass
