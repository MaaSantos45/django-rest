# Generated by Django 5.0.6 on 2024-08-06 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_category_options_alter_recipe_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
    ]
