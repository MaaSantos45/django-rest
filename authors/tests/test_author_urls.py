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
