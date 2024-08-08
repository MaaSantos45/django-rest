from django.urls import reverse, resolve
from recipes.views import site
from . import RecipeTestBase

# Create your tests here.


class RecipeViewTests(RecipeTestBase):
    def test_recipes_home_view_function(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, site.RecipeHomeView)

    def test_recipes_home_view_function_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_category_view_function(self):
        view = resolve(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertIs(view.func.view_class, site.RecipeHomeView)

    def test_recipes_category_view_function_template(self):
        response = self.client.get(reverse('recipes:category', kwargs={'id_category': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_detail_view_function(self):
        view = resolve(reverse('recipes:recipe_details', kwargs={'id_recipe': 1}))
        self.assertIs(view.func.view_class, site.RecipeDetailView)

    def test_recipes_detail_view_function_template(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:recipe_details', kwargs={'id_recipe': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/recipe-detail.html')

    def test_recipes_search_view_function(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func.view_class, site.RecipeSearchView)

    def test_recipes_search_view_function_template(self):
        response = self.client.get(reverse('recipes:search'), data={'q': 'test'})
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
