from . import BaseTestClass
from app.auth.models import User
from app.models import Post

class BlogClientTestCase(BaseTestClass):

    def test_index_with_no_posts(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'No hay entradas', res.data)

    def test_index_with_posts(self):
        """Verifica que, cuando ya haya una entrada, se muestre en el index"""
        with self.app.app_context():
                admin = User.get_by_email('admin@xyz.com')
                post = Post(user_id=admin.id, title='Post de prueba', content='Lorem Ipsum')
                post.save()
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)
        self.assertNotIn(b'No hay entradas', res.data)

    def test_redirect_to_login_page_if_not_logged_in(self):
        """Verifica que, si no esta logueado, se redirija a la pagina de login"""
        res = self.client.get('/admin/')
        self.assertEqual(302, res.status_code)
        self.assertIn('login', res.location)

    def test_unauthorized_access_to_admin(self):
        """Verifica que, si no es administrados, no pueda acceder a la pagina de admin"""
        self.login('guest@xyz.com', '1111')
        res = self.client.get('/admin/')
        self.assertEqual(401, res.status_code)
        self.assertIn(b'Ooops!! No tienes permisos de acceso', res.data)

    def test_authorized_access_to_admin(self):
        """Verifica que, un administrador efectivamente entre a la pagina de admin"""
        self.login('admin@xyz.com', '1111')
        res = self.client.get('/admin/')
        self.assertEqual(200, res.status_code)
        self.assertIn(b'Posts', res.data)
        self.assertIn(b'Usuarios', res.data)