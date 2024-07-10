from django.urls import reverse
from . import AuthorTestBase

# Create your tests here.


class AuthorURLsTests(AuthorTestBase):
    def test_author_url_register(self):
        url = reverse('authors:register')
        self.assertEqual(url, '/authors/')

    def test_author_url_login(self):
        url = reverse('authors:login')
        self.assertEqual(url, '/authors/login/')

    def test_author_url_logout(self):
        url = reverse('authors:logout')
        self.assertEqual(url, '/authors/logout/')

    def test_author_url_profile(self):
        url = reverse('authors:profile')
        self.assertEqual(url, '/authors/profile/')

    def test_author_url_create_recipe(self):
        url = reverse('authors:create_recipe')
        self.assertEqual(url, '/authors/profile/recipe/create/')

    def test_author_url_edit_recipe(self):
        url = reverse('authors:edit_recipe', kwargs={'id_recipe': 1})
        self.assertEqual(url, '/authors/profile/recipe/edit/1/')

    def test_author_url_delete_recipe(self):
        url = reverse('authors:delete_recipe', kwargs={'id_recipe': 1})
        self.assertEqual(url, '/authors/profile/recipe/delete/1/')
