from django.test import TestCase
from usuarios.models import Usuario
import datetime
from django.contrib.auth.models import Group

class UsuarioModelTest(TestCase):
    def setUp(self):
        cargos = ["DIRETOR", "NTI", "COORDENADOR", "SECRETARIO", "NAPI", "MANUTENCAO"]
        for cargo in cargos:
            Group.objects.create(name=cargo)
        self.usuario = Usuario.objects.create_user(
            matricula='111111',
            nome='Brayan',
            email_institucional='brayan@ifpi.edu.br',
            telefone='86999999999',
            data_nascimento=datetime.date(2000, 1, 1),
            sexo='M',
            cargo='NTI',
            password='123',
        )

    def test_usuario(self):
        self.assertEqual(self.usuario.matricula, '111111')

    def test_login(self):
        login_ok = self.client.login(username='111111', password='123')
        self.assertTrue(login_ok)

    def test_logout(self):
        logout_ok = self.client.logout()
        self.assertIsNone(logout_ok)