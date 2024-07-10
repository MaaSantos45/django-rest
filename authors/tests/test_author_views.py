from django.urls import reverse, resolve
from authors import views
from . import AuthorTestBase

# Create your tests here.


class AuthorViewTests(AuthorTestBase):
    def setUp(self):
        self.username = "Test.Author"
        # noinspection HardcodedPassword
        self.password = "Str0ngP@ss"
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_author_register_view_function(self):
        view = resolve(reverse('authors:register'))
        self.assertIs(view.func, views.register)

    def test_author_register_view_function_template(self):
        response = self.client.get(reverse('authors:register'))
        self.assertTemplateUsed(response, 'authors/pages/register.html')

    def test_author_login_view_function(self):
        view = resolve(reverse('authors:login'))
        self.assertIs(view.func, views.login)

    def test_author_login_view_function_template(self):
        response = self.client.get(reverse('authors:login'))
        self.assertTemplateUsed(response, 'authors/pages/login.html')

    def test_author_logout_view_function(self):
        view = resolve(reverse('authors:logout'))
        self.assertIs(view.func, views.logout)

    def test_author_logout_view_function_template(self):
        response = self.client.get(reverse('authors:logout'), follow=True)
        self.assertTemplateUsed(response, 'authors/pages/login.html')

    def test_author_profile_view_function(self):
        view = resolve(reverse('authors:profile'))
        self.assertIs(view.func, views.profile)

    def test_author_profile_view_function_template(self):
        self.make_author(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('authors:profile'), follow=True)
        self.assertTemplateUsed(response, 'authors/pages/profile.html')

    def test_author_create_recipe_view_function(self):
        view = resolve(reverse('authors:create_recipe'))
        self.assertIs(view.func, views.create_recipe)

    def test_author_create_recipe_view_function_template(self):
        self.make_author(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('authors:create_recipe'), follow=True)
        self.assertTemplateUsed(response, 'authors/pages/recipe-detail.html')

    def test_author_edit_recipe_view_function(self):
        view = resolve(reverse('authors:edit_recipe', kwargs={'id_recipe': 1}))
        self.assertIs(view.func, views.edit_recipe)

    def test_author_edit_recipe_view_function_template(self):
        self.make_recipe(author_data={'username': self.username, 'password': self.password})
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('authors:edit_recipe', kwargs={'id_recipe': 1}), follow=True)
        self.assertTemplateUsed(response, 'authors/pages/recipe-detail.html')

    def test_author_delete_recipe_view_function(self):
        view = resolve(reverse('authors:delete_recipe', kwargs={'id_recipe': 1}))
        self.assertIs(view.func, views.delete_recipe)

    def test_author_delete_recipe_view_function_template(self):
        self.make_recipe(author_data={'username': self.username, 'password': self.password})
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('authors:delete_recipe', kwargs={'id_recipe': 1}), follow=True)
        self.assertTemplateUsed(response, 'authors/pages/profile.html')
