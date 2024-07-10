from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/recipe/create/', views.create_recipe, name='create_recipe'),
    path('profile/recipe/edit/<id_recipe>/', views.edit_recipe, name='edit_recipe'),
    path('profile/recipe/delete/<id_recipe>/', views.delete_recipe, name='delete_recipe'),
]
