import os

from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # Debugging to confirm config is loaded
    #print("Config Loaded: ", app.config)


    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)


    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.vehicle import bp as vehicle_bp
    app.register_blueprint(vehicle_bp)

    return app
    
from app import models
