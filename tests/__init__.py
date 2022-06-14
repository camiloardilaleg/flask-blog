import unittest

from app import create_app, db
from app.auth.models import User

class BaseTestClass(unittest.TestCase):

    # Ejecuta codigo antes de cada test
    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client() # Es el cliente que nos brinda la API de Flask

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()
            # Create admin user
            BaseTestClass.create_user('admin', 'admin@xyz.com', '1111', True)
            # Create guest user
            BaseTestClass.create_user('guest', 'guest@xyz.com', '1111', False)


    # ejecuta codigo despues de cada test
    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos al finalizar el test
            db.session.remove()
            db.drop_all()

    @staticmethod
    def create_user(name, email, password, is_admin):
        user = User(name=name, email=email)
        user.set_password(password)
        user.is_admin = is_admin
        user.save()
        return user
