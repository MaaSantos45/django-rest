from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from recipes.models import Recipe
from utils.pagination import make_pagination


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-created_at', '-updated_at']
    template_name = None

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, context.get('recipes'))

        context.update({'recipes': page_obj, 'pagination_range': pagination_range})
        return context


class RecipeHomeView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.kwargs.get('id_category') is not None:
            qs = qs.filter(category__id=self.kwargs.get('id_category'))
        return qs


class RecipeHomeViewApi(RecipeHomeView):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes'].object_list.values()

        return JsonResponse({
            'recipes': list(recipes),
            'len': len(recipes),
        })


class RecipeSearchView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q_term = None

    def get(self, *args, **kwargs):
        self.q_term = self.request.GET.get('q', '').strip()
        if not self.q_term:
            return redirect(reverse('recipes:home'))
        return super().get(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(is_published=True)
        terms = self.q_term.split(' ')
        for term in terms:
            qs = qs.filter(
                Q(title__icontains=term) |
                Q(slug__icontains=term) |
                Q(description__icontains=term) |
                Q(author__first_name__icontains=term) |
                Q(author__last_name__icontains=term) |
                Q(author__username__icontains=term) |
                Q(category__name__icontains=term)
            )

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(self.request, context.get('object_list'), per_page=10,
                                                     qtd_pages=10)
        context.update({'recipes': page_obj, 'pagination_range': pagination_range, 'q_term': self.q_term})
        return context


class RecipeTagView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(is_published=True)
        qs = qs.filter(
            Q(tags__slug=self.kwargs.get('slug', ''))
        )
        return qs


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-detail.html'
    pk_url_kwarg = 'id_recipe'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        qs = qs.select_related('author', 'category',)
        qs = qs.prefetch_related('tags',)

        return qs.filter(is_published=True)


class RecipeDetailViewApi(RecipeDetailView):
    template_name = 'recipes/pages/recipe-detail.html'

    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        created_at, updated_at = recipe.created_at, recipe.updated_at

        recipe = model_to_dict(recipe, exclude=['is_published'])
        recipe['created_at'] = created_at
        recipe['updated_at'] = updated_at

        if recipe.get('cover'):
            recipe['cover'] = self.request.build_absolute_uri()[:-1] + recipe['cover'].url

        return JsonResponse({
            'recipe': recipe,
        })
