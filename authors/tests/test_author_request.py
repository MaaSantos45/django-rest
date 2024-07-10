from unittest import skip
from unittest.mock import patch

from recipes.models import Recipe
from . import AuthorTestBase
from parameterized import parameterized
from authors import forms
from django.urls import reverse
from django.contrib.auth.models import User
from urllib.parse import quote_plus
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


class AuthorRequestRecipeTest(AuthorTestBase):
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
            'title': 'Recipe Title',
            'description': 'Recipe Description',
            'category': 1,
            'preparation_time': 5,
            'preparation_time_unit': 'minutes',
            'preparation_steps': 'This is the preparation steps for the recipe test.',
            'servings': 1,
            'servings_unit': 'portion',
        }
        self.login_form_data = {
            'username': 'JohnTest',
            'password': 'Str0ngP@ss',
        }

    def tearDown(self):
        self.client.post(reverse('authors:logout'), follow=True)
        return super().tearDown()

    @patch('utils.pagination.PER_PAGE', new=3)
    def test_author_request_profile_logged_with_recipes(self):
        author = User.objects.filter(username=self.login_form_data['username']).first()
        recipes_ids = [r.id for r in self.make_recipes_qtd(6, user=author)]
        recipes = Recipe.objects.filter(id__in=recipes_ids).order_by('-created_at').order_by('-updated_at')

        self.client.login(**self.login_form_data)

        response = self.client.get(reverse('authors:profile'), follow=True)

        recipes_in = recipes[:3]
        recipes_out = recipes[3:]

        recipes_context = response.context['recipes'].object_list

        for recipe in recipes_in:
            self.assertIn(recipe, recipes_context)

        for recipe in recipes_out:
            self.assertNotIn(recipe, recipes_context)

    @parameterized.expand([
        reverse('authors:profile'),
        reverse('authors:create_recipe'),
        reverse('authors:edit_recipe', kwargs={'id_recipe': 1}),
        reverse('authors:delete_recipe', kwargs={'id_recipe': 1}),
    ])
    def test_author_request_profile_crud_recipes_not_logged(self, reversed_url):
        self.make_recipe()
        response = self.client.get(reversed_url, follow=True)
        url = quote_plus(reversed_url)
        self.assertRedirects(response, reverse('authors:login') + f'?next={url}', status_code=302, target_status_code=200)

    def test_author_request_logged_create_recipe_form_invalid(self):
        self.client.login(**self.login_form_data)
        self.form_data['title'] = 'A' * 4
        self.form_data['description'] = 'A' * 4
        response = self.client.post(reverse('authors:create_recipe'), data=self.form_data, follow=True)

        expected_content_title = f"title: Title must be at least 5 characters."
        expected_content_description = f"description: Description must be at least 5 characters."
        expected_content = f"fields: Description cannot be equal to title."

        self.assertIn(expected_content, response.content.decode())
        self.assertIn(expected_content_title, response.content.decode())
        self.assertIn(expected_content_description, response.content.decode())

    def test_author_request_logged_create_recipe_form_valid(self):
        self.make_category()
        self.client.login(**self.login_form_data)
        response = self.client.post(reverse('authors:create_recipe'), data=self.form_data, follow=True)

        expected_content = 'Recipe Created, wait until review'
        self.assertIn(expected_content, response.content.decode())

    def test_author_request_logged_edit_recipe_form_invalid_with_recipe(self):
        del self.form_data['category']
        self.client.login(**self.login_form_data)

        author = User.objects.get(pk=self.client.session.get('_auth_user_id', 1))
        self.make_recipe(**self.form_data, current_user=author)

        self.form_data['title'] = 'A' * 4
        self.form_data['description'] = 'A' * 4
        self.form_data['category'] = 1

        response = self.client.get(reverse('authors:edit_recipe', kwargs={'id_recipe': 1}), follow=True)
        expected_content = html.escape("Recipe already published, if you update, it'll be unpublished for review")
        self.assertIn(expected_content, response.content.decode())

        response = self.client.post(reverse('authors:edit_recipe', kwargs={'id_recipe': 1}), data=self.form_data, follow=True)

        expected_content_title = f"title: Title must be at least 5 characters."
        expected_content_description = f"description: Description must be at least 5 characters."
        expected_content = f"fields: Description cannot be equal to title."

        self.assertIn(expected_content, response.content.decode())
        self.assertIn(expected_content_title, response.content.decode())
        self.assertIn(expected_content_description, response.content.decode())

    def test_author_request_logged_edit_recipe_form_valid(self):
        del self.form_data['category']
        self.client.login(**self.login_form_data)

        author = User.objects.get(pk=self.client.session.get('_auth_user_id', 1))
        self.make_recipe(**self.form_data, current_user=author)

        self.form_data['title'] = 'Title Updated'
        self.form_data['category'] = 1

        response = self.client.post(reverse('authors:edit_recipe', kwargs={'id_recipe': 1}), data=self.form_data, follow=True)
        expected_content = html.escape("Recipe updated, wait until review")
        self.assertIn(expected_content, response.content.decode())

        response = self.client.get(reverse('authors:edit_recipe', kwargs={'id_recipe': 1}), follow=True)
        unexpected_content = html.escape("Recipe already published, if you update, it'll be unpublished for review")
        self.assertNotIn(unexpected_content, response.content.decode())

    def test_author_request_logged_delete_recipe_form_valid(self):
        del self.form_data['category']
        self.client.login(**self.login_form_data)

        author = User.objects.get(pk=self.client.session.get('_auth_user_id', 1))
        self.make_recipe(**self.form_data, current_user=author)

        response = self.client.post(reverse('authors:delete_recipe', kwargs={'id_recipe': 1}), follow=True)
        expected_content = html.escape("Recipe deleted")
        self.assertIn(expected_content, response.content.decode())

    @parameterized.expand([
        (reverse('authors:edit_recipe', kwargs={'id_recipe': 2})),
        (reverse('authors:delete_recipe', kwargs={'id_recipe': 2})),
    ])
    def test_author_request_logged_invalid_recipe_get(self, reversed_url):
        del self.form_data['category']
        self.client.login(**self.login_form_data)

        author = User.objects.get(pk=self.client.session.get('_auth_user_id', 1))
        self.make_recipe(**self.form_data, current_user=author)

        self.form_data['category'] = 1

        response = self.client.post(reversed_url, data=self.form_data, follow=True)
        expected_content = html.escape("No recipe found")
        self.assertIn(expected_content, response.context['exception'])
        self.assertEqual(response.status_code, 404)
