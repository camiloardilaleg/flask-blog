from .default import *

# Parámetros para activar el modo debug
TESTING = True
DEBUG = True

APP_ENV = APP_ENV_TESTING
WTF_CSRF_ENABLED = False # deshabilita la protección CSRF durante los tests


# SQLALCHEMY_DATABASE_URI = 'postgresql://db_user:db_pass@host:port/db_name'