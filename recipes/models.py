from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    description = models.CharField(max_length=165)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=10, choices={'minutes': "Minutes", 'hours': "Hours"})
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=10, choices={'portion': "Portion", 'people': "People"})
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to="recipes/covers/%Y/%m/%d", blank=True)

    def __str__(self):
        return self.title
