from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
swagger = Swagger()

def create_app(config_name):
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    from app.api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
