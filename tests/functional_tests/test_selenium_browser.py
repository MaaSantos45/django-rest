from django.test import LiveServerTestCase
from utils.browser import make_browser
import pytest


@pytest.mark.functional_test
class SeleniumTest(LiveServerTestCase):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_browser_headless(self):
        self.browser = make_browser('--headless')
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by="tag name", value='body')
        self.assertIn('No Recipes Published.', body.text)
        self.browser.quit()
