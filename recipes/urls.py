from django.urls import path
from .views import site, api

app_name = 'recipes'

urlpatterns = [
    path('', site.RecipeHomeView.as_view(), name='home'),
    path('recipes/api/v1/', site.RecipeHomeViewApi.as_view(), name='home_api'),
    path('recipes/search/', site.RecipeSearchView.as_view(), name='search'),
    path('category/<int:id_category>/', site.RecipeHomeView.as_view(), name='category'),
    path('tags/<slug:slug>/', site.RecipeTagView.as_view(), name='tag'),
    path('recipe-details/<int:id_recipe>/', site.RecipeDetailView.as_view(), name='recipe_details'),
    path('recipes/api/v1/<int:id_recipe>/', site.RecipeDetailViewApi.as_view(), name='recipe_details_api'),
]

urlpatterns += [
    path('api/v2/recipes/', api.api_recipe_list, name='api_recipes'),
    path('api/v2/recipes/tag/<int:pk>/', api.api_recipes_tag, name='api_recipes_tag'),
    path('api/v2/recipes/<int:pk>/', api.api_recipe_detail, name='api_recipe_detail'),
]
