from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from utils.browser import make_browser
from recipes.tests import RecipeMixin
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import pytest
import time


class BaseFunctionalTests(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_browser()
        self.actions = ActionChains(self.browser)
        return super().setUp

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    @staticmethod
    def sleep(seconds: int | float = 5):
        time.sleep(seconds)

    def get_by_id(self, id_):
        return self.browser.find_element(By.ID, id_)

    def get_by_css(self, selector):
        return self.browser.find_element(By.CSS_SELECTOR, selector)

    def get_by_name(self, name):
        return self.browser.find_element(By.NAME, name)

    def scroll_to(self, element, sec: int | float = 0.2):
        self.browser.execute_script("arguments[0].scrollIntoView()", element)
        self.sleep(sec)

    def move_to(self, element):
        self.actions.move_to_element(element).perform()


@pytest.mark.functional_test
class RecipeBaseFuncTest(BaseFunctionalTests, RecipeMixin):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


@pytest.mark.functional_test
class AuthorBaseFuncTest(BaseFunctionalTests):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()
