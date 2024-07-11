from django.views.generic import View, TemplateView
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from authors import forms
from recipes import models as recipe_models
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(login_url='authors:login'), name='dispatch')
class DashboardView(View):

    def get_recipe(self, id_recipe=None):
        if id_recipe is None:
            return None
        recipe = recipe_models.Recipe.objects.filter(id=id_recipe, author=self.request.user).first()
        if not recipe:
            raise Http404('No recipe found')
        return recipe

    def get_form(self, recipe):
        form = forms.AuthorRecipeForm(data=self.request.POST or None, files=self.request.FILES or None, instance=recipe)

        if form.errors:
            for field, errors in form.errors.items():
                if field == '__all__':
                    field = 'fields'
                messages.error(self.request, f"{field}: {', '.join(errors)}")
        return form

    def render_recipe(self, form, recipe):
        if recipe is not None and recipe.is_published:
            messages.warning(self.request, "Recipe already published, if you update, it'll be unpublished for review")
        return render(self.request, 'authors/pages/recipe-detail.html', context={"recipe": recipe, 'form': form})

    def get(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('id_recipe'))
        form = self.get_form(recipe)
        return self.render_recipe(form, recipe)

    def post(self, *args, **kwargs):
        recipe_instance = self.get_recipe(kwargs.get('id_recipe'))
        form = self.get_form(recipe_instance)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = self.request.user
            recipe.is_published = False
            recipe.preparation_steps_is_html = False

            recipe.cover = self.request.FILES.get('cover')

            recipe.save()
            if recipe_instance is None:
                messages.success(self.request, 'Recipe Created, wait until review')
            else:
                messages.success(self.request, 'Recipe updated, wait until review')
            return redirect(reverse('authors:profile'))
        return self.render_recipe(form, recipe_instance)


@method_decorator(login_required(login_url='authors:login'), name='dispatch')
class DashboardViewDelete(DashboardView):
    def get(self, *args, **kwargs):
        return redirect(reverse('authors:profile'))

    def post(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('id_recipe'))
        recipe.delete()
        messages.success(self.request, 'Recipe deleted')

        return redirect(reverse('authors:profile'))
