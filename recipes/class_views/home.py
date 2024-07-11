from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
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
        page_obj, pagination_range = make_pagination(self.request, context.get('object_list'), per_page=10, qtd_pages=10)
        context.update({'recipes': page_obj, 'pagination_range': pagination_range, 'q_term': self.q_term})
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-detail.html'
    pk_url_kwarg = 'id_recipe'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(is_published=True)
