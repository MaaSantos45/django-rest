from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common import exceptions as ex
from django.contrib.auth.models import User
from django.urls import reverse
from unittest import skip
from . import AuthorBaseFuncTest


@skip
class AuthorRegisterFuncTest(AuthorBaseFuncTest):
    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_author_register_valid_inputs(self):
        self.browser.get(self.live_server_url + '/authors/')

        username = self.get_by_css('input#id_username')
        username.send_keys('UserName')

        first_name = self.get_by_css('input#id_first_name')
        first_name.send_keys('FirstName')

        last_name = self.get_by_css('input#id_last_name')
        last_name.send_keys('LastName')

        email = self.get_by_css('input#id_email')
        email.send_keys('e-mail@test.com')

        password = self.get_by_css('input#id_password')
        password.send_keys('Str0ngP@ss')

        confirm_password = self.get_by_css('input#id_confirm_password')
        confirm_password.send_keys('Str0ngP@ss')

        submit = self.browser.find_element(By.CSS_SELECTOR, 'form>button[type="submit"]')

        # self.scroll(submit)
        self.move_to(submit)

        submit.click()

        self.sleep(1)
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Successfully Registered', body)
        self.assertIn('Login', body)

    @parameterized.expand([
        ('username', 'username: Must not be empty'),
        ('password', 'password: This field is required.'),
        ('confirm_password', 'confirm_password: This field is required.'),
    ])
    def test_author_register_blank_inputs(self, field_name, error_missing):
        def fill_form(form_):
            fields = form_.find_elements(By.TAG_NAME, 'input')
            for field in fields:
                if field.is_displayed():
                    field.send_keys('Aa1!' * 20)

            self.get_by_name('email').send_keys('a@email.com')

        self.browser.get(self.live_server_url + '/authors/')
        form = self.get_by_id('form')
        fill_form(form)

        field_tested = self.get_by_name(field_name)
        self.actions.double_click(field_tested).click().perform()
        field_tested.send_keys(' ')
        form.submit()

        self.sleep(1)
        self.assertIn(error_missing, self.get_by_css('body').text)

    @parameterized.expand([
        ('A1!A1!A1!A1!A1!', "password: Password isn't strong enough"),
        ('Aa1!Aa1!A1!A1!A1!', "password: Don't use your username 'Aa1!Aa1!A1!A1!A1!' as password", "fields: The password and confirmation is required."),
        ('Aa1!Ab1!A1!A1!A1!', "fields: The two password fields didn't match.")
    ])
    def test_author_register_invalid_inputs(self, password_value, password_error, confirm_error=None):
        self.browser.get(self.live_server_url + '/authors/')
        form = self.get_by_id('form')

        username = self.get_by_css('input#id_username')
        username.send_keys('Aa1!Aa1!A1!A1!A1!')
        username_expected = 'username: Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'

        first_name = self.get_by_css('input#id_first_name')
        first_name.send_keys('F' * 15)

        last_name = self.get_by_css('input#id_last_name')
        last_name.send_keys('L' * 15)

        email = self.get_by_css('input#id_email')
        email.send_keys('e-mailtest.com')
        email_expected = 'email: Enter a valid email address.'

        password = self.get_by_css('input#id_password')
        password.send_keys(password_value)
        password_expected = password_error

        confirm_password = self.get_by_css('input#id_confirm_password')
        if 'b' in password_value:
            confirm_password.send_keys('Aa1!Aa1!A1!A1!A1!')
            confirm_password_expected = password_error
        else:
            confirm_password.send_keys(' ')
            confirm_password_expected = "confirm_password: This field is required."

        if confirm_error is not None:
            fields_expected = confirm_error
        else:
            fields_expected = password_error

        form.submit()
        self.sleep(1)
        body = self.get_by_css('body').text

        for expected in [username_expected, email_expected, password_expected, confirm_password_expected, fields_expected]:
            self.assertIn(expected, body)


class AuthorLoginFuncTest(AuthorBaseFuncTest):
    def setUp(self):
        self.suser = 'User.Test'
        self.spass = 'Str0ngP@ss'
        self.user = User.objects.create_user(
            username=self.suser,
            password=self.spass,
        )
        return super().setUp()

    def tearDown(self):
        User.objects.all().delete()
        return super().tearDown()

    def test_author_login_valid_user_valid_password(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.get_by_id('form')

        username = self.get_by_css('input#id_username')
        username.send_keys(self.suser)

        password = self.get_by_css('input#id_password')
        password.send_keys(self.spass)

        form.submit()
        self.sleep(1)

        body = self.get_by_css('body').text
        self.assertIn('Login Successful', body)

    def test_author_login_valid_user_invalid_password(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.get_by_id('form')

        username = self.get_by_css('input#id_username')
        username.send_keys(self.suser)

        password = self.get_by_css('input#id_password')
        password.send_keys(self.spass + 'Wrong')

        form.submit()
        self.sleep(1)

        body = self.get_by_css('body').text
        self.assertIn('Invalid Credentials', body)

    def test_author_login_invalid_user(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.get_by_id('form')

        username = self.get_by_css('input#id_username')
        username.send_keys(self.suser + 'Wrong')

        password = self.get_by_css('input#id_password')
        password.send_keys(self.spass)

        form.submit()
        self.sleep(1)

        body = self.get_by_css('body').text
        self.assertIn('fields: Username or password is incorrect.', body)

    def test_author_login_blank_username_and_password(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.get_by_id('form')

        username = self.get_by_css('input#id_username')
        username.send_keys(' ')

        password = self.get_by_css('input#id_password')
        password.send_keys(' ')

        form.submit()
        self.sleep(1)

        body = self.get_by_css('body').text
        print(body)
        self.assertIn('fields: Username or password is incorrect.', body)
        self.assertIn('username: This field is required.', body)
        self.assertIn('password: This field is required.', body)
