from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/recipe/create/', views.DashboardView.as_view(), name='create_recipe'),
    path('profile/recipe/edit/<int:id_recipe>/', views.DashboardView.as_view(), name='edit_recipe'),
    path('profile/recipe/delete/<int:id_recipe>/', views.DashboardViewDelete.as_view(), name='delete_recipe'),
]
