from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
login_manager = LoginManager()
db = SQLAlchemy()


def create_app(settings_module):
    
    # Initialize the app
    app = Flask(__name__, instance_relative_config=True) #le digo que instance esta al mismo nivel que la app
    
    # config file
    app.config.from_object(settings_module)

    if app.config.get('TESTING', False):
        app.config.from_pyfile('config_tesing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)
    
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" # <-- Define la vista que se va a mostrar cuando el usuario no esté logueado
    db.init_app(app)
    
    # Registro de los Blueprints
    from .auth import auth_bp
    app.register_blueprint(auth_bp)
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    from .public import public_bp
    app.register_blueprint(public_bp)
    
    return app


"""
if app.config.get('TESTING', False): -> retorna False si 'TESTING' no esta definido
"""