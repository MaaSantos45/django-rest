from unittest import skip
from . import AuthorTestBase
from parameterized import parameterized
from authors import forms
from django.urls import reverse
import html


class AuthorFormRegisterUnitTest(AuthorTestBase):
    def setUp(self):
        self.form = forms.AuthorRegisterForm()

    @parameterized.expand([
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
        ('username', 'Username'),
        ('email', 'e-mail@example.com'),
        ('password', 'Password'),
        ('confirm_password', 'Confirm Password'),
    ])
    def test_form_placeholder_fields(self, field, expected):
        placeholder = self.form.fields[field].widget.attrs.get('placeholder')
        self.assertEqual(placeholder, expected)

    @parameterized.expand([
        ('username', 'Required.'),
        ('password', 'must contain at least 8 characters, lower and upper letters, numbers and special characters.'),
        ('first_name', ''),
        ('last_name', ''),
        ('email', ''),
        ('confirm_password', ''),
    ])
    def test_form_help_text_fields(self, field, expected):
        help_text = self.form.fields[field].help_text
        self.assertEqual(help_text, expected)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('confirm_password', 'Confirm Password'),
    ])
    def test_form_label_fields(self, field, expected):
        label = self.form.fields[field].label
        self.assertEqual(label, expected)


class AuthorFormRegisterIntegrationTest(AuthorTestBase):
    def setUp(self):
        self.form_data = {
            'first_name': 'New',
            'last_name': 'User Test',
            'username': 'new.user',
            'email': 'e-mail@test.com',
            'password': 'Str0ngP@ss',
            'confirm_password': 'Str0ngP@ss',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'Must not be empty.'),
        ('password', 'This field is required.'),
        ('confirm_password', 'This field is required.'),
    ])
    def test_form_fields_empty(self, field, expected):
        self.form_data[field] = ''
        expected_content = f"{field}: {expected}"
        response = self.client.post(reverse('authors:register'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())

    @parameterized.expand([
        ('username', 150),
        ('first_name', 150),
        ('last_name', 150),
        ('email', 254),
        ('password', 128),
        ('confirm_password', 128),
    ])
    def test_form_fields_max_length(self, field, expected):
        expected_char = 'Must be less than or equal to %s characters.' % expected
        string_max = 'A' * (expected + 1)
        self.form_data[field] = string_max

        if field == 'email':
            self.form_data[field] = string_max[:100] + string_max[112:] + '@exemple.com'

        expected_content = f"{field}: {expected_char}"
        response = self.client.post(reverse('authors:register'), data=self.form_data)

        self.assertIn(expected_content, response.content.decode())

    def test_form_week_password(self):
        self.form_data['password'] = '123abc'
        expected_content = html.escape("Password isn't strong enough")
        response = self.client.post(reverse('authors:register'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())

    def test_form_different_confirm_password(self):
        self.form_data['password'] = 'aBc123!!'
        self.form_data['confirm_password'] = 'aBc123!@'
        expected_content = html.escape("The two password fields didn't match.")
        response = self.client.post(reverse('authors:register'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())

    def test_form_password_and_confirm_password_equal(self):
        self.form_data['password'] = 'aBc123!!'
        self.form_data['confirm_password'] = 'aBc123!!'

        expected_content = html.escape("Successfully Registered")
        unexpected_content1 = html.escape("The two password fields didn't match.")
        unexpected_content2 = html.escape("Password isn't strong enough")

        response = self.client.post(reverse('authors:register'), data=self.form_data, follow=True)
        self.assertIn(expected_content, response.content.decode())
        self.assertNotIn(unexpected_content1, response.content.decode())
        self.assertNotIn(unexpected_content2, response.content.decode())

    def test_form_username_in_password(self):
        self.form_data['username'] = 'NewUser'
        self.form_data['password'] = 'NewUser123$!'
        self.form_data['confirm_password'] = 'NewUser123$!'

        expected_content = html.escape("Don't use your username 'NewUser' as password")
        response = self.client.post(reverse('authors:register'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())

    def test_form_email_unique_equal(self):
        response_first_user = self.client.post(reverse('authors:register'), data=self.form_data, follow=True)
        self.assertIn(html.escape("Successfully Registered"), response_first_user.content.decode())

        self.form_data['username'] = 'AnotherUser'
        expected_content = html.escape("email: This email is already registered.")
        unexpected_content = html.escape("Successfully Registered")

        response = self.client.post(reverse('authors:register'), data=self.form_data, follow=True)
        self.assertIn(expected_content, response.content.decode())
        self.assertNotIn(unexpected_content, response.content.decode())

    def test_user_can_login(self):
        self.client.post(reverse('authors:register'), data=self.form_data)

        is_authenticated = self.client.login(
            username=self.form_data['username'],
            password=self.form_data['password']
        )

        self.assertTrue(is_authenticated)


class AuthorFormLoginTest(AuthorTestBase):
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
        ('username', 'JohnTestIncorrect'),
        ('password', 'StrongP@ss'),
    ])
    def test_form_login_clean_fields(self, field, value):
        self.form_data[field] = value

        expected = html.escape('fields: Username or password is incorrect.')
        response = self.client.post(reverse('authors:login'), data=self.form_data)
        self.assertIn(expected, response.content.decode())


class AuthorRecipeFormTest(AuthorTestBase):
    def setUp(self):
        self.make_category()
        self.client.post(reverse('authors:register'), {
            'first_name': 'New',
            'last_name': 'User Test',
            'username': 'JohnTest',
            'email': 'e-mail@test.com',
            'password': 'Str0ngP@ss',
            'confirm_password': 'Str0ngP@ss',
        })

        self.login_form_data = {
            'username': 'JohnTest',
            'password': 'Str0ngP@ss',
        }

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
        return super().setUp()

    def tearDown(self):
        self.client.post(reverse('authors:logout'))
        return super().tearDown()

    @parameterized.expand([
        ('title', 'This field is required.'),
        ('description', 'This field is required.'),
        ('category', 'This field is required.'),
        ('preparation_time', 'This field is required.'),
        ('preparation_time_unit', 'This field is required.'),
        ('preparation_steps', 'This field is required.'),
        ('servings', 'This field is required.'),
        ('servings_unit', 'This field is required.'),
    ])
    def test_form_fields_empty(self, field, expected):
        self.form_data[field] = ''
        expected_content = f"{field}: {expected}"
        self.client.login(**self.login_form_data)

        response = self.client.post(reverse('authors:create_recipe'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())

    @parameterized.expand([
        ('preparation_time', 'Preparation time must be greater than 0.'),
        ('servings', 'Servings must be greater than 0.'),
    ])
    def test_form_fields_negative(self, field, expected):
        self.form_data[field] = -1
        expected_content = f"{field}: {expected}"
        self.client.login(**self.login_form_data)

        response = self.client.post(reverse('authors:create_recipe'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())

    @parameterized.expand([
        ('preparation_time', 'Enter a whole number., Preparation time must be greater than 0.'),
        ('servings', 'Enter a whole number., Servings must be greater than 0.'),
    ])
    def test_form_fields_invalids(self, field, expected):
        self.form_data[field] = 'ab'
        expected_content = f"{field}: {expected}"
        self.client.login(**self.login_form_data)

        response = self.client.post(reverse('authors:create_recipe'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())

    def test_form_fields_short(self):
        self.form_data['title'] = 'A' * 4
        self.form_data['description'] = 'A' * 4

        expected_content_title = f"title: Title must be at least 5 characters."
        expected_content_description = f"description: Description must be at least 5 characters."
        self.client.login(**self.login_form_data)

        response = self.client.post(reverse('authors:create_recipe'), data=self.form_data)
        self.assertIn(expected_content_title, response.content.decode())
        self.assertIn(expected_content_description, response.content.decode())

    def test_form_fields_equal(self):
        self.form_data['title'] = 'A' * 5
        self.form_data['description'] = 'A' * 5

        expected_content = f"fields: Description cannot be equal to title."
        self.client.login(**self.login_form_data)

        response = self.client.post(reverse('authors:create_recipe'), data=self.form_data)
        self.assertIn(expected_content, response.content.decode())
