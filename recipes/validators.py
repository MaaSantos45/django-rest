from collections import defaultdict
from django.core import exceptions
import inspect


class RecipeValidator:
    def __init__(self, data, errors=None, error_class=None):
        self.data = data
        self.errors = defaultdict(list) if errors is None else errors
        self.error_class = exceptions.ValidationError if error_class is None else error_class

        self.clean()

    def clean(self):
        members = inspect.getmembers(self.__class__, predicate=lambda x: inspect.ismethod(x) or inspect.isfunction(x))
        for name, member in members:
            if name.startswith('clean_'):
                clean_field = getattr(self, name)
                clean_field()

        data = self.data

        try:
            preparation_time = int(data.get('preparation_time'))
        except (TypeError, ValueError):
            preparation_time = 0

        if preparation_time <= 0:
            self.errors['preparation_time'].append('Preparation time must be greater than 0.')

        try:
            servings = int(data.get('servings'))
        except (TypeError, ValueError):
            servings = 0

        if servings <= 0:
            self.errors['servings'].append('Servings must be greater than 0.')

        if len(data.get('title', '')) < 5:
            self.errors['title'].append('Title must be at least 5 characters.')

        if len(data.get('description', '')) < 5:
            self.errors['description'].append('Description must be at least 5 characters.')

        if data.get('description', '') == data.get('title', ''):
            self.errors['__all__'].append('Description cannot be equal to title.')

        if self.errors:
            raise self.error_class(self.errors)
