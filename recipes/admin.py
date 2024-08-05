from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from . import models
# from tags.models import Tag

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    ...


# class TagInline(GenericStackedInline):
#     model = Tag
#     fields = ('name', )
#
#     extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'updated_at', 'is_published',)
    list_display_links = ('id', 'title')

    search_fields = ('slug', 'title', 'author__username', 'author__first_name', 'author__last_name', 'description',)

    list_filter = ('is_published', 'category', 'preparation_steps_is_html',)
    list_editable = ('is_published',)

    ordering = ('-updated_at',)
    prepopulated_fields = {'slug': ('title', 'author')}

    list_per_page = 10

    # inlines = [TagInline, ]
    autocomplete_fields = ('tags', )


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
