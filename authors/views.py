from django.shortcuts import render, redirect
from django.http import Http404
from django.core import exceptions as exp
from django.urls import reverse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from recipes import models as recipe_models
from utils.pagination import make_pagination
from django.views.generic import View, TemplateView
from django.utils.decorators import method_decorator
from . import forms, models

# Create your views here.


def register(request):
    form = forms.AuthorRegisterForm(request.POST or None)

    if form.errors:
        for field, errors in form.errors.items():
            if field == '__all__':
                field = 'fields'
            messages.error(request, f"{field}: {', '.join(errors)}")

    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Successfully Registered')
        return redirect('authors:login')

    return render(request, 'authors/pages/register.html', context={'form': form, 'form_action': reverse('authors:register')})


def login(request):
    form = forms.AuthorLoginForm(request.POST or None)

    if form.errors:
        for field, errors in form.errors.items():
            if field == '__all__':
                field = 'fields'
            messages.error(request, f"{field}: {', '.join(errors)}")

    if request.method == 'POST' and form.is_valid():
        user = auth.authenticate(
            request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )

        if user:
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            return redirect(reverse('recipes:home'))
        messages.error(request, 'Invalid Credentials')

    return render(request, 'authors/pages/login.html', context={'form': form, 'form_action': reverse('authors:login')})


@login_required(login_url='authors:login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Logout Successful')
    return redirect(reverse('authors:login'))


# @login_required(login_url='authors:login')
# def profile(request):
#     recipes = recipe_models.Recipe.objects.filter(author=request.user).order_by('-created_at').order_by('-updated_at')
#     page_obj, pagination_range = make_pagination(request, recipes)
#     return render(request, 'authors/pages/profile.html', context={'recipes': page_obj, 'pagination_range': pagination_range})
@method_decorator(login_required(login_url='authors:login'), name='dispatch')
class ProfileView(TemplateView):
    template_name = 'authors/pages/profile.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        recipes = recipe_models.Recipe.objects.filter(author=self.request.user)
        recipes = recipes.order_by('-created_at').order_by('-updated_at')
        recipes = recipes.select_related('author', 'category')
        page_obj, pagination_range = make_pagination(self.request, recipes)

        profile = models.Profile.objects.filter(author=self.request.user).select_related('author').first()
        if profile is None:
            profile = models.Profile(author=self.request.user)
            profile.save()

        context['recipes'] = page_obj
        context['pagination_range'] = pagination_range
        context['profile'] = profile

        return self.render_to_response(context)


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
        else:
            print(form)
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
