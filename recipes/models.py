from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=100, choices={'minutes': "Minutes", 'hours': "Hours"})
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField()
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=100, choices={'portion': "Portion", 'people': "People"})
    is_published = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover = models.ImageField(upload_to="recipes/covers/%Y/%m/%d", blank=True)

    def __str__(self):
        return self.title
