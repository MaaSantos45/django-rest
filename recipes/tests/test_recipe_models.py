import django.core.exceptions as e
from unittest import skip
from parameterized import parameterized
from . import RecipeTestBase
from recipes import models


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = models.Recipe(
            author=self.make_author(username='newauthor'),
            category=self.make_category(name='test category'),
            title='Test Recipe',
            description='Test Recipe Description',
            servings=3,
            servings_unit="portion",
            slug='test-recipe-new',
            preparation_time=30,
            preparation_time_unit="minutes",
            preparation_steps="Lorem Ipsu...",
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_model_title_str(self):
        self.assertEqual(str(self.recipe), self.recipe.title)

    def test_category_model_name_str(self):
        category = self.make_category()
        self.assertEqual(str(category), category.name)

    # using subTest
    # def test_recipe_model_fields_max_length(self):
    #     fields = [
    #         ('title', 65),
    #         ('description', 165),
    #     ]
    #
    #     for field, max_length in fields:
    #         with self.subTest(field=field, max_length=max_length):
    #             setattr(self.recipe, field, 'A' * (max_length + 0))
    #             with self.assertRaises(e.ValidationError):
    #                 self.recipe.full_clean()

    # using parameterized
    @parameterized.expand([
        ('title', 65),
        ('description', 165),
    ])
    def test_recipe_model_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(e.ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('name', 60),
    ])
    def test_category_model_fields_max_length(self, field, max_length):
        category = models.Category()
        setattr(category, field, 'A' * (max_length + 1))
        with self.assertRaises(e.ValidationError):
            category.full_clean()

    @skip('Need to validate choices')
    def test_recipe_model_fields_choice(self):
        self.recipe.preparation_time_unit = "hours"

        # self.assertRaises(django.core.exceptions.ValidationError, self.recipe.full_clean)
        with self.assertRaises(e.ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        "preparation_steps_is_html",
        "is_published",
    ])
    def test_recipe_model_fields_default_false(self, field):
        recipe = self.make_recipe_no_defaults()

        self.assertFalse(getattr(recipe, field))
