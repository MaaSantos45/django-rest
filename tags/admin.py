from django.contrib import admin
from tags import models

# Register your models here.


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'slug')

    search_fields = ('name', 'slug')
    list_per_page = 10
    list_editable = ('name', )

    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.Tag, TagAdmin)
