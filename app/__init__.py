import os

from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager 
from flask_socketio import SocketIO


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
socketio = SocketIO(cors_allowed_origins="*", async_mode="eventlet")


def create_app(config_class=Config):
    app = Flask(__name__)
    
    flask_env = os.getenv('FLASK_ENV', 'production')
    if flask_env == 'development':
        app.config.from_object('config.DevelopmentConfig')
    else:
        app.config.from_object('config.ProductionConfig')

    # Debugging to confirm correct config is loaded
    print(f"FLASK_ENV: {flask_env}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")


    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    socketio.init_app(app, async_mode="eventlet")


    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.activity_planner import bp as activity_planner_bp
    app.register_blueprint(activity_planner_bp)

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    from app.meal_planner import bp as meal_planner_bp
    app.register_blueprint(meal_planner_bp)
    

    from app.vehicle import bp as vehicle_bp
    app.register_blueprint(vehicle_bp)

    return app
    
from app import models
from app.sockets import socketio
