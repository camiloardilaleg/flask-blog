import unittest

from app import create_app, db

class BaseTestClass(unittest.TestCase):

    # Ejecuta codigo antes de cada test
    def setUp(self):
        self.app = create_app(settings_module="config.testing")
        self.client = self.app.test_client() # Es el cliente que nos brinda la API de Flask

        # Crea un contexto de aplicación
        with self.app.app_context():
            # Crea las tablas de la base de datos
            db.create_all()

    # ejecuta codigo despues de cada test
    def tearDown(self):
        with self.app.app_context():
            # Elimina todas las tablas de la base de datos al finalizar el test
            db.session.remove()
            db.drop_all()