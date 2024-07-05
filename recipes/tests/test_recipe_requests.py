from django.urls import reverse, resolve
from recipes import views, models
from unittest.mock import patch
from . import RecipeTestBase
import pytest
import utils


class RecipeRequestHomeTests(RecipeTestBase):
    def test_recipe_request_home_without_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes Published.', response.content)

    def test_recipe_request_home_with_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Recipe', response.content)
        self.assertEqual(len(response.context['recipes']), 1)

    def test_recipe_request_home_with_recipe_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes Published.', response.content)

    @patch('utils.pagination.PER_PAGE', new=5)
    @pytest.mark.slow
    def test_recipe_request_home_is_paginated(self):
        self.make_recipes_qtd(20)

        response = self.client.get(reverse("recipes:home"))
        paginator = response.context['recipes'].paginator

        self.assertEqual(paginator.num_pages, 4)
        self.assertEqual(paginator.per_page, 5)
        self.assertEqual(len(paginator.get_page(1)), 5)


class RecipeRequestCategoryTests(RecipeTestBase):
    def test_recipe_request_category_without_recipes(self):
        response = self.client.get(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes Published.', response.content)

    def test_recipe_request_category_with_recipes(self):
        title = "Test Title Recipe"
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(title.encode(), response.content)

    def test_recipe_request_category_with_recipe_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes Published.', response.content)


class RecipeRequestDetailTests(RecipeTestBase):
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

    @pytest.mark.slow
    def test_recipe_request_recipe_with_recipe_not_published(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe_details', kwargs={'id_recipe': 1}))
        self.assertEqual(response.status_code, 404)


class RecipeRequestSearchTests(RecipeTestBase):
    def test_recipe_request_search_without_q(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertRedirects(response, reverse('recipes:home'))

    def test_recipe_request_search_q_scaped(self):
        response = self.client.get(reverse('recipes:search'), data={'q': '<script>alert("1")</script>'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"&lt;script&gt;alert(&quot;1&quot;)&lt;/script&gt;"', response.content)

    def test_recipe_request_search_without_recipes(self):
        response = self.client.get(reverse('recipes:search'), data={'q': 'testnofound'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No Recipes Published.', response.content)

    def test_recipe_request_search_with_recipes(self):
        recipe1 = self.make_recipe(author_data={'username': 'Other Author'})
        recipe2 = self.make_recipe(slug='outra_recipe', title='Outra Recipe')

        response1 = self.client.get(reverse('recipes:search'), data={'q': 'Other Author'})
        self.assertEqual(response1.status_code, 200)
        self.assertIn(b'Other Author', response1.content)
        self.assertEqual(len(response1.context['recipes']), 1)

        response2 = self.client.get(reverse("recipes:search"), data={'q': 'Outra Recipe'})
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        response3 = self.client.get(reverse("recipes:search"), data={'q': 'Test Recipe'})
        self.assertIn(recipe1, response3.context['recipes'])
        self.assertIn(recipe2, response3.context['recipes'])
