from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
from . import RecipeBaseFuncTest


class RecipeHomePageFuncTest(RecipeBaseFuncTest):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_open_home_without_recipes(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')

        self.assertIn('No Recipes Published.', body.text)

    @patch('utils.pagination.PER_PAGE', new=10)
    def test_open_home_with_recipes(self):
        self.make_recipes_qtd(20)

        # User open the home
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')

        self.assertNotIn('No Recipes Published.', body.text)
        self.assertIn('Test Recipe', body.text)

        # User see the search input
        search_input = self.browser.find_element(by=By.CSS_SELECTOR, value='#search-input')
        search_input.click()

        # User type title in search
        search_input.send_keys('Test Recipe 1')
        search_input.send_keys(Keys.ENTER)

        # User see the result
        self.assertNotIn(
            'Test Recipe 2',
            self.browser.find_element(by=By.TAG_NAME, value='body').text
        )
        for i in range(9):
            self.assertIn(
                f'Test Recipe 1{i}',
                self.browser.find_element(by=By.TAG_NAME, value='body').text
            )

    @patch('utils.pagination.PER_PAGE', new=10)
    def test_recipe_open_home_pagination(self):
        recipes = self.make_recipes_qtd(12)

        # User open the home
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')
        for recipe in recipes[2:]:
            self.assertIn(recipe.title + '\n', body.text)

        # User see the pagination
        page_link = self.browser.find_element(by=By.CSS_SELECTOR, value='a[href="/?page=2"]')
        page_link.click()

        # User see the result
        recipes_pg_2 = len(self.browser.find_elements(By.CLASS_NAME, 'card'))
        self.assertEqual(len(recipes[:2]), recipes_pg_2)
