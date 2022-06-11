from logging.handlers import SMTPHandler
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
login_manager = LoginManager()
db = SQLAlchemy()

import logging

def create_app(settings_module):
    
    # Initialize the app
    app = Flask(__name__, instance_relative_config=True) #le digo que instance esta al mismo nivel que la app
    
    # config file
    app.config.from_object(settings_module)

    if app.config.get('TESTING', False):
        app.config.from_pyfile('config_tesing.py', silent=True)
    else:
        app.config.from_pyfile('config.py', silent=True)
    
    # set up logging handlers
    configure_logging(app)
    
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

    #Custom error handlers
    register_error_handlers(app)
      
    return app

def register_error_handlers(app):
    
    @app.errorhandler(401)
    def error_401_handler(error):
        return render_template('401.html'), 401

    @app.errorhandler(404)
    def error_404_handler(error):
        return render_template('404.html'), 404 # <-- Retorna una tupla con el template y el STATUS CODE
    
    @app.errorhandler(500)
    def error_500_handler(error):
        return render_template('500.html'), 500
        


def configure_logging(app):
    
    # Eliminamos los posibles manejadores, si existen, del logger por defecto
    del app.logger.handlers[:]
    
    # Añadimos el logger por defecto a la lista de loggers
    loggers = [app.logger, logging.getLogger('sqlalchemy'), logging.getLogger('flask_login')]
    handlers = []
    
    # Creamos un manejador para escribir los mensajes por consola
    console_handler = logging.StreamHandler() # <-- Manejador de mensajes por consola
    console_handler.setFormatter(verbose_formatter())
        # console_handler.setLevel(logging.DEBUG)
    # handlers.append(console_handler)

    # Configure depending on the environment
    if (app.config['APP_ENV'] == app.config['APP_ENV_LOCAL']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_TESTING']) or (
            app.config['APP_ENV'] == app.config['APP_ENV_DEVELOPMENT']):
        console_handler.setLevel(logging.DEBUG)
        handlers.append(console_handler)
    elif app.config['APP_ENV'] == app.config['APP_ENV_PRODUCTION']:
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        # Configure mail server to send error to admin
        mail_handler = SMTPHandler(
            (app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            app.config['DONT_REPLY_EMAIL'], 
            app.config['ADMINS'],
            '[ERROR][{}] La aplicacion fallo'.format(app.config['APP_ENV']),
            (app.config('MAIL_USERNAME'), app.config('MAIL_PASSWORD')),
            ()
        )

        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(mail_handler_formatter())
        handlers.append(mail_handler)
    
    # Asociamos cada uno de los handlers a cada uno de los loggers
    for l in loggers:
        for handler in handlers:
            l.addHandler(handler)
        l.propagate = False
        l.setLevel(logging.DEBUG)

def verbose_formatter():
    return logging.Formatter(
        '[%(asctime)s.%(msecs)d]\t %(levelname)s \t[%(name)s.%(funcName)s:%(lineno)d]\t %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

def mail_handler_formatter():
    return logging.Formatter(
        '''
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s.%(msecs)d
            Message:
            %(message)s
        ''',
        datefmt='%d/%m/%Y %H:%M:%S'
    )

"""
if app.config.get('TESTING', False): -> retorna False si 'TESTING' no esta definido

2. Es importante notar como el orden de las funciones no tiene tanta importancia. Es decir, que podemos definir
una funcion x(a,b) que toma como paramentros a,b, y definir posteriormente las funciones a, b y no pasa nada.
Es decir, que primero se cargan todas las funciones y luego se ejecutan.
"""