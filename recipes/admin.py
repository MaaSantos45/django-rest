from django.contrib import admin
from . import models

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'updated_at', 'is_published',)
    list_display_links = ('id', 'title')

    search_fields = ('slug', 'title', 'author', 'description',)
    list_filter = ('is_published', 'category', 'preparation_steps_is_html',)
    list_editable = ('is_published',)

    ordering = ('-updated_at',)
    prepopulated_fields = {'slug': ('title', 'author')}

    list_per_page = 10


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
