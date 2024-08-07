from django.db import models
from django.contrib.auth.models import User
# from django.contrib.contenttypes import fields
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from random import choice
from tags.models import Tag
from PIL import Image
import io
import os


# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=70)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    # tags = fields.GenericRelation(Tag, related_query_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)

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

    def get_absolute_url(self):
        return reverse('recipes:recipe_details', kwargs={'id_recipe': self.id})

    def resize_img(self, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, self.cover.name)
        try:
            image = Image.open(image_full_path)
        except FileNotFoundError:
            return None

        old_width, old_height = image.size

        if old_width > new_width:
            new_height = round((new_width * old_height) / old_width)

            new_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            new_image.save(
                image_full_path,
                optimize=True,
                quality=100,
            )

    def save(self, *args, **kwargs):
        slug = slugify(str(self.title) + "-" + str(self.author.id))

        while Recipe.objects.all().filter(slug=slug).first():
            slug += choice('abcdefghijklmnopkrstuvwxyz')
        self.slug = slug

        save = super().save(*args, **kwargs)

        if self.cover:
            self.resize_img()

        return save
