from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class AccountsViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_data = {
            'username': 'user_1',
            'email': 'test_1@example.com',
            'password': '1234567890!',
            'password_confirmed': '1234567890!',
        }

        self.created_user = User.objects.create_user(
            username='user', email='test@example.com', password='1234567890!'
        )

        refresh = RefreshToken.for_user(self.created_user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

    def test_register_user(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_existing_username(self):
        self.user_data = {
            'username': 'user',
            'email': 'test@example.com',
            'password': '1234567890!',
            'password_confirmed': '1234567890!',
        }
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_login_user(self):
        data = {"username": "user", "password": "1234567890!"}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["tokens"])
        self.assertIn("refresh", response.data["tokens"])

    def test_login_invalid_credentials(self):
        data = {"username": "user", "password": "1234567890"}
        response = self.client.post(reverse("login"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_change_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        data = {
            "old_password": "1234567890!",
            "new_password": "1234567890!!",
        }
        response = self.client.post(reverse("change-password"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Password changed successfully.")
        self.created_user.refresh_from_db()
        self.assertFalse(self.created_user.check_password("1234567890!"))
        self.assertTrue(self.created_user.check_password("1234567890!!"))

    def test_change_password_invalid_old_password(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        data = {
            "old_password": "1234567890",
            "new_password": "1234567890!",
        }
        response = self.client.post(reverse("change-password"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        data = {"refresh": self.refresh_token}
        response = self.client.post(reverse("logout"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Successfully logged out.")

    def test_logout_invalid_refresh_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        data = {"refresh": "invalid_refresh_token"}
        response = self.client.post(reverse("logout"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
