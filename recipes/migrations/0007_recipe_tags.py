# Generated by Django 5.0.6 on 2024-08-05 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_recipe_slug'),
        ('tags', '0002_remove_tag_content_type_remove_tag_object_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_query_name='recipes', to='tags.tag'),
        ),
    ]
