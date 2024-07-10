from django.test import TestCase

from recipes import models, tests


class AuthorTestBase(TestCase, tests.RecipeMixin):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
