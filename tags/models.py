from django.contrib.contenttypes import fields
from django.db import models
from random import choice
from django.utils.text import slugify

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    content_type = models.ForeignKey(fields.ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = fields.GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        slug = slugify(str(self.name))
        while Tag.objects.all().filter(slug=slug).first():
            slug += choice('abcdefghijklmnopkrstuvwxyz')
        self.slug = slug
        return super().save(*args, **kwargs)
