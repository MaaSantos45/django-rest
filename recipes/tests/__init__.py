from django.test import TestCase
from recipes import models


class RecipeMixin:
    @staticmethod
    def make_category(name='Category Test'):
        return models.Category.objects.create(name=name)

    @staticmethod
    def make_author(username='test.test', password='123ABCabc@', first_name='John', last_name='Doe'):
        return models.User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

    def make_recipe(
            self,
            author_data=None,
            category_data=None,
            title='Test Recipe',
            description='Test Recipe Description',
            servings=3,
            servings_unit="portion",
            slug='test-recipe',
            preparation_time=30,
            preparation_time_unit="minutes",
            preparation_steps="Lorem Ipsu...",
            preparation_steps_is_html=False,
            is_published=True,
    ):
        if author_data is None:
            author_data = {}

        if category_data is None:
            category_data = {}

        return models.Recipe.objects.create(
            author=self.make_author(**author_data),
            category=self.make_category(**category_data),
            title=title,
            description=description,
            servings=servings,
            servings_unit=servings_unit,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipes_qtd(self, qtd=10):
        recipes = []
        for i in range(qtd):
            kwargs = {"author_data": {"username": f"TestPage-{i}"}, "title": f"Test Recipe {i}", "slug": f"test-slug-{i}"}
            recipes.append(self.make_recipe(**kwargs))
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

