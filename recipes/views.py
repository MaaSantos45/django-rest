from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from utils.recipes.factory import make_recipes
from . import models

# Create your views here.


def home(request, id_category=None):

    recipes = models.Recipe.objects.all().order_by('-created_at').order_by('-updated_at')
    recipes = recipes.filter(is_published=True)
    if id_category is not None:
        recipes = recipes.filter(category__id=id_category)
    return render(request, "recipes/pages/home.html", context={'recipes': recipes})


def recipe_detail(request, id_recipe):
    recipe = models.Recipe.objects.filter(id=id_recipe).first()
    if not recipe:
        raise Http404('No recipe found')
    return render(request, "recipes/pages/recipe-detail.html", context={"recipe": recipe})
