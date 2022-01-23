from django.test import TestCase, Client
from faker import Faker
from random import randint

from .models import User


class AuthTestCase(TestCase):
    def setUp(self):
        faker = Faker()

        self.test_user_data = {
            'email': faker.unique.email(),
            'password': faker.unique.password(),
            'bonus_balance': randint(1, 25),
        }

        self.premade_user_data = {
            'email': faker.unique.email(),
            'password': faker.unique.password(),
            'bonus_balance': randint(1, 25),
        }
        self.fake_password = faker.unique.password()
        self.new_password = faker.unique.password()

        User.objects.create_user(*self.premade_user_data.values())

        self.client = Client()

    def test_register_user(self):
        register_url = '/api/auth/register'

        # Test without any data in request body
        response = self.client.post(register_url)
        status_code = response.status_code

        self.failIf(status_code != 400,
                    f'Register request without body responded with status code {status_code}')

        # Test with correct data
        response = self.client.post(register_url, self.test_user_data)
        status_code = response.status_code

        self.failIf(status_code != 201,
                    f'Failed to register with correct data. Status code {status_code}')

        data = response.json()
        self.assertEqual(self.test_user_data['email'], data['email'])

        user = User.objects.get(email=data['email'])
        self.assertTrue(user.check_password(
            self.test_user_data['password']), 'Password not matched')

    def test_access_token(self):
        token_obtain_url = '/api/auth/token'
        check_token_url = '/api/auth/user/1'

        # Test without any data in request body
        response = self.client.post(token_obtain_url)
        status_code = response.status_code

        self.failIf(status_code != 400,
                    f'Obtain token request without body responded with status code {status_code}')

        # Test token obtain with correct data
        response = self.client.post(token_obtain_url, self.premade_user_data)
        status_code = response.status_code

        self.failIf(status_code != 200,
                    f"Failed to login with correct data. Status code {status_code}")

        data = response.json()

        access_token = data['access']

        response = self.client.get(
            check_token_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        status_code = response.status_code

        self.failIf(status_code != 200,
                    f'Failed to authenticate with correct access token. Status code {status_code}')

    def test_refresh_access_token(self):
        token_obtain_url = '/api/auth/token'
        token_refresh_url = '/api/auth/token/refresh'
        check_token_url = '/api/auth/user/1'  # 1 is user id

        # Obtain JWT tokens
        response = self.client.post(token_obtain_url, self.premade_user_data)
        data = response.json()
        access_token, refresh_token = data['access'], data['refresh']

        # Test without any data in request body
        response = self.client.post(token_refresh_url)
        status_code = response.status_code

        self.failIf(status_code != 400,
                    f'Obtain token request without body responded with status code {status_code}')

        # Test with correct data
        response = self.client.post(
            token_refresh_url, {'refresh': refresh_token})
        status_code = response.status_code

        self.failIf(status_code != 200,
                    f'Failed to refresh token. Status code {status_code}')

        data = response.json()
        refreshed_access_token = data['access']

        response = self.client.get(
            check_token_url, HTTP_AUTHORIZATION=f'Bearer {refreshed_access_token}')
        status_code = response.status_code

        self.failIf(status_code != 200,
                    f'Failed to authenticate with refreshed access token. Status code {status_code}')

    def test_change_password(self):
        register_url = '/api/auth/register'
        obtain_access_token_url = '/api/auth/token'
        change_password_url = '/api/auth/change-password/2'  # 1 is user id

        # Register user
        self.client.post(register_url, self.test_user_data)

        # Obtain JWT access token
        response = self.client.post(
            obtain_access_token_url, self.test_user_data)
        access_token = response.json()['access']

        # Test with incorrect password
        response = self.client.patch(change_password_url, {
            'old_password': self.fake_password,
            'new_password': self.new_password
        }, 'application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        status_code = response.status_code

        self.failIf(status_code != 400,
                    f'Request with incorrect password responded with status different from 400. Status code {status_code}')

        # Test with correct password
        response = self.client.patch(change_password_url, {
            'old_password': self.test_user_data['password'],
            'new_password': self.new_password
        }, 'application/json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        status_code = response.status_code

        self.failIf(status_code != 200,
                    f'Request failed with correct data. Status code {status_code}')

        # Test login with new password
        response = self.client.post(obtain_access_token_url, {
            'email': self.test_user_data['email'],
            'password': self.new_password
        })
        status_code = response.status_code

        self.failIf(status_code != 200,
                    f'Failed to login with new passsword. Status code {status_code}')
