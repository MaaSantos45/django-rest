from django.urls import reverse
from . import RecipeTestBase

# Create your tests here.


class RecipeURLsTests(RecipeTestBase):
    def test_recipes_url_home(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipes_url_category(self):
        url = reverse('recipes:category', kwargs={'id_category': 1})
        self.assertEqual(url, '/category/1/')

    def test_recipes_url_recipe_details(self):
        url = reverse('recipes:recipe_details', kwargs={'id_recipe': 1})
        self.assertEqual(url, '/recipe-details/1/')
