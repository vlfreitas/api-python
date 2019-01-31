import unittest
from app import create_app, db


class UsersTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="test")
        self.client = self.app.test_client
        self.user = {"username": "Unittest1", "email": "unittest1@example.com"}
        with self.app.app_context():
            db.create_all()

    def test_get_user(self):
        """ Teste para retornar um usuário """
        result = self.client().get('/api/users/1')
        self.assertEqual(result.status_code, 200)

    def test_post_user(self):
        """ Teste para criar um usuário """
        result = self.client().post("/api/users", data=self.user)
        self.assertEqual(result.status_code, 201)

    def test_bad_request_post_user_(self):
        """ Teste para criar um usuário, porém o mesmo ja existe """
        result = self.client().post("/api/users", data=self.user)
        self.assertEqual(result.status_code, 400)

    def test_get_user_filmes(self):
        """ Teste para consumir a API do OMDb e retornar o filme solicitado """
        result = self.client().get("/api/users/1/filme?&s=superman")
        self.assertEqual(result.status_code, 200)
