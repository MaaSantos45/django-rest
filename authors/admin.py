from django.contrib import admin
from authors.models import Profile

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    ...


admin.site.register(Profile, AuthorAdmin)
