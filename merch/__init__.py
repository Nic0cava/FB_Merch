# merch/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
app.register_blueprint(items)
app.register_blueprint(category)
app.register_blueprint(core)
app.register_blueprint(error_pages)