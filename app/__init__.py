from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from .models import db
import routes

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    Migrate(app, db)

    # Register routes
    app.register_blueprint(routes.main)

    return app
