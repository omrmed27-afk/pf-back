from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.authentication import services


class AuthServicesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="auth_user", password="correct_pass")

    def test_login_valid_credentials_returns_token(self):
        token = services.login("auth_user", "correct_pass")
        self.assertIsNotNone(token)
        self.assertIsInstance(token, Token)

    def test_login_wrong_password_returns_none(self):
        token = services.login("auth_user", "wrong_pass")
        self.assertIsNone(token)

    def test_login_nonexistent_user_returns_none(self):
        token = services.login("no_existe", "pass")
        self.assertIsNone(token)

    def test_login_creates_token_if_not_exists(self):
        self.assertFalse(Token.objects.filter(user=self.user).exists())
        services.login("auth_user", "correct_pass")
        self.assertTrue(Token.objects.filter(user=self.user).exists())

    def test_login_returns_existing_token(self):
        existing = Token.objects.create(user=self.user)
        token = services.login("auth_user", "correct_pass")
        self.assertEqual(token.key, existing.key)

    def test_logout_deletes_token(self):
        Token.objects.create(user=self.user)
        services.logout(self.user)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_without_token_does_not_raise(self):
        services.logout(self.user)  # no token exists — should not raise
