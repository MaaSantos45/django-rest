from django.urls import reverse, resolve
from authors import views
from . import AuthorTestBase

# Create your tests here.


class AuthorViewTests(AuthorTestBase):
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
