from unittest import skip
from . import AuthorTestBase
from parameterized import parameterized
from authors import forms
from django.urls import reverse
import html


class AuthorRequestAuthTest(AuthorTestBase):
    def setUp(self):
        self.client.post(reverse('authors:register'), {
            'first_name': 'New',
            'last_name': 'User Test',
            'username': 'JohnTest',
            'email': 'e-mail@test.com',
            'password': 'Str0ngP@ss',
            'confirm_password': 'Str0ngP@ss',
        })

        self.form_data = {
            'username': 'JohnTest',
            'password': 'Str0ngP@ss',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'username: This field is required.'),
        ('password', 'password: This field is required.')
    ])
    def test_author_request_login_form_invalid(self, field, expected):
        self.form_data[field] = ''
        response = self.client.post(reverse('authors:login'), data=self.form_data, follow=True)

        self.assertIn(expected, response.content.decode())

    def test_author_request_login_form_valid_without_user_password(self):
        self.form_data['password'] += "Wrong"
        response = self.client.post(reverse('authors:login'), data=self.form_data, follow=True)

        self.assertIn('Invalid Credentials', response.content.decode())

    def test_author_request_login_form_valid_user(self):
        response = self.client.post(reverse('authors:login'), data=self.form_data, follow=True)

        self.assertIn('Login Successful', response.content.decode())

    def test_author_request_logout_get(self):
        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertRedirects(response, reverse('authors:login') + f'?next={reverse('authors:logout')}', status_code=302, target_status_code=200)
        self.assertNotIn('Logout Successful', response.content.decode())

        self.client.post(reverse('authors:login'), data=self.form_data)
        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertRedirects(response, reverse('authors:login'), status_code=302, target_status_code=200)
        self.assertNotIn('Logout Successful', response.content.decode())

    def test_author_request_not_logged_logout_post(self):
        response = self.client.post(reverse('authors:logout'), follow=True)
        self.assertRedirects(response, reverse('authors:login') + f'?next={reverse('authors:logout')}', status_code=302, target_status_code=200)

        self.assertNotIn('Logout Successful', response.content.decode())

    def test_author_request_logged_logout_post(self):
        self.client.post(reverse('authors:login'), data=self.form_data)

        response = self.client.post(reverse('authors:logout'), follow=True)
        self.assertRedirects(response, reverse('authors:login'), status_code=302, target_status_code=200)

        self.assertIn('Logout Successful', response.content.decode())
