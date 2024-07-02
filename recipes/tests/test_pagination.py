from . import RecipeTestBase
from utils.pagination import make_pagination_range
from django.urls import reverse


class RecipePaginationTest(RecipeTestBase):
    def test_make_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=10,
            current_page=1,
        )
        self.assertEqual(list(range(1, 11)), pagination['pagination'])

    def test_first_range_static_if_current_less_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=10,
            current_page=1,
        )
        self.assertEqual(list(range(1, 11)), pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=10,
            current_page=5,
        )
        self.assertEqual(list(range(1, 11)), pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=10,
            current_page=6,
        )
        self.assertEqual(list(range(2, 12)), pagination['pagination'])

    def test_lest_range_static_if_current_more_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=10,
            current_page=14,
        )
        self.assertEqual(list(range(10, 20)), pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=10,
            current_page=15,
        )
        self.assertEqual(list(range(11, 21)), pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qtd_pages=10,
            current_page=20,
        )
        self.assertEqual(list(range(11, 21)), pagination['pagination'])

    def test_recipe_pagination_request_page_invalid(self):
        for i in list(range(20)):
            self.make_recipe({"username": f"TestPage-{i}"}, slug=f"test-slug-{i}")

        response = self.client.get(reverse("recipes:home"), data={"page": "string"})
        current_page = response.context['pagination_range']['current_page']

        self.assertEqual(current_page, 1)
