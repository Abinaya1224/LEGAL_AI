from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config


app = Flask(__name__)
app.config.from_object(config)


# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Import the routes and models
from app import routes, models