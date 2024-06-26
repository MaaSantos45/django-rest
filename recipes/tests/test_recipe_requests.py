from django.urls import reverse, resolve
from recipes import views, models
from . import RecipeTestBase


class RecipeRequestTests(RecipeTestBase):
    # def setUp(self):
    #     return super().setUp()
    #
    # def tearDown(self):
    #     return super().tearDown()

    def test_recipe_request_home_without_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes published.', response.content)

    def test_recipe_request_home_with_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Recipe', response.content)
        self.assertEqual(len(response.context['recipes']), 1)

    def test_recipe_request_category_without_recipes(self):
        response = self.client.get(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes published.', response.content)

    def test_recipe_request_category_with_recipes(self):
        title = "Test Title Recipe"
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(title.encode(), response.content)

    def test_recipe_request_recipe_without_recipe(self):
        response = self.client.get(reverse('recipes:recipe_details', kwargs={'id_recipe': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_request_recipe_with_recipe(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:recipe_details', kwargs={'id_recipe': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Recipe', response.content)

    def test_recipe_request_recipe_context(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:recipe_details', kwargs={'id_recipe': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipe'].title, 'Test Recipe')

    def test_recipe_request_home_with_recipe_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes published.', response.content)

    def test_recipe_request_category_with_recipe_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes published.', response.content)

    def test_recipe_request_recipe_with_recipe_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe_details', kwargs={'id_recipe': 1}))
        self.assertEqual(response.status_code, 404)
