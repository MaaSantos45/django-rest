from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core import exceptions as exp
from recipes import models as recipe_models
from secrets import compare_digest
from collections import defaultdict
import re


class AuthorRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.add_attr('last_name', 'placeholder', 'Last Name')

        self.fields['password'].validators.append(self.validator_strong_password)

    confirm_password = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        }),
        error_messages={
            'required': 'This field is required.',
            'max_length': 'Must be less than or equal to 128 characters.',
        },
        max_length=128
    )

    @staticmethod
    def validator_strong_password(password):
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%*()_+^&}{:;?.])[0-9a-zA-Z!@#$%*()_+^&}{:;?.]{8,}$"
        match_strong = re.search(pattern, password)

        if match_strong is None:
            raise exp.ValidationError(
                "Password isn't strong enough",
                code='invalid',
            )

    def add_attr(self, field_name, attr_name, attr_new_value):
        existing_attrs = self.fields[field_name].widget.attrs.get(attr_name, '')
        self.fields[field_name].widget.attrs[attr_name] = f'{existing_attrs} {attr_new_value}'.strip()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

        labels = {'email': 'E-mail'}

        help_texts = {
            'username': 'Required.',
            'password': 'must contain at least 8 characters, lower and upper letters, numbers and special characters.',
        }

        error_messages = {
            'username': {
                'unique': 'A user with that username already exists.',
                'required': 'Must not be empty.',
                'max_length': 'Must be less than or equal to 150 characters.',
            },

            'first_name': {
                'max_length': 'Must be less than or equal to 150 characters.',
            },

            'last_name': {
                'max_length': 'Must be less than or equal to 150 characters.',
            },

            'email': {
                'max_length': 'Must be less than or equal to 254 characters.',
            },

            'password': {
                'max_length': 'Must be less than or equal to 128 characters.',
            }
        }

        max_length = {
            'password': 128,
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control'
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'placeholder': 'e-mail@example.com',
                'class': 'form-control'
            }),

            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }),
        }

    def clean_password(self):
        data = self.cleaned_data.get('password', '')
        username = self.cleaned_data.get('username', '')

        if username and username in data:
            raise exp.ValidationError(
                "Don't use your username '%(value)s' as password",
                code='invalid',
                params={'value': username}
            )

        return data

    def clean_email(self):
        data = self.cleaned_data.get('email', '')
        exist = User.objects.filter(email=data).exists()

        if exist:
            raise exp.ValidationError(
                "This email is already registered.",
                code="invalid"
            )

        return data

    def clean(self):
        cleand_data = super().clean()

        passwd = cleand_data.get('password', '')
        confirm_passwd = cleand_data.get('confirm_password', '')

        if not passwd or not confirm_passwd:
            raise exp.ValidationError(
                "The password and confirmation is required.",
            )

        if not compare_digest(passwd, confirm_passwd):
            raise exp.ValidationError(
                "The two password fields didn't match.",
            )


class AuthorLoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].widget.attrs['class'] = 'form-control'

        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password'].widget.attrs['class'] = 'form-control'

    username = forms.CharField(
        required=True,
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput()
    )

    def clean(self):
        cleand_data = super().clean()

        usernm = cleand_data.get('username', '')
        passwd = cleand_data.get('password', '')

        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%*()_+^&}{:;?.])[0-9a-zA-Z!@#$%*()_+^&}{:;?.]{8,}$"
        match_strong = re.search(pattern, passwd)

        user = User.objects.filter(username=usernm).exists()
        if not user or not match_strong:
            raise exp.ValidationError(
                f"Username or password is incorrect.",
            )


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self._form_erros = defaultdict(list)
        super().__init__(*args, **kwargs)

    class Meta:
        model = recipe_models.Recipe
        exclude = ['author', 'is_published', 'preparation_steps_is_html', 'created_at', 'updated_at', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Title',
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'preparation_time': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'preparation_time_unit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'preparation_steps': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'servings_unit': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cover': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        data = self.cleaned_data
        try:
            preparation_time = int(data.get('preparation_time'))
        except (TypeError, ValueError):
            preparation_time = 0

        if preparation_time <= 0:
            self._form_erros['preparation_time'].append('Preparation time must be greater than 0.')

        try:
            servings = int(data.get('servings'))
        except (TypeError, ValueError):
            servings = 0

        if servings <= 0:
            self._form_erros['servings'].append('Servings must be greater than 0.')

        if len(data.get('title', '')) < 5:
            self._form_erros['title'].append('Title must be at least 5 characters.')

        if len(data.get('description', '')) < 5:
            self._form_erros['description'].append('Description must be at least 5 characters.')

        if data.get('description', '') == data.get('title', ''):
            self._form_erros['__all__'].append('Description cannot be equal to title.')

        if self._form_erros:
            raise exp.ValidationError(self._form_erros)

        return super().clean()
