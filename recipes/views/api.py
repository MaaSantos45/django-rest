from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from recipes import models, serializers, permissions
from utils.pagination import RecipePagination


# class ApiRecipeList(APIView):
#     def get(self, request):
#         recipes = models.Recipe.objects.all().order_by('-created_at').order_by('-updated_at')
#         recipes = recipes.select_related('author', 'category').prefetch_related('tags')
#         serializer = serializers.RecipeSerializer(instance=recipes, many=True, context={'request': self.request})
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = serializers.RecipeSerializer(data=self.request.data, context={'request': self.request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


# class ApiRecipeDetail(APIView):
#
#     @staticmethod
#     def get_object(pk):
#         if not pk:
#             # return Response({'detail': 'Missing primary key'}, status=status.HTTP_400_BAD_REQUEST)
#             response = APIException('Missing primary key')
#             response.status_code = status.HTTP_400_BAD_REQUEST
#             raise response
#
#         recipe = models.Recipe.objects.filter(
#             pk=pk
#         ).select_related('author', 'category').prefetch_related('tags').first()
#
#         if not recipe:
#             # return Response({'detail': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)
#             response = APIException('Recipe not found')
#             response.status_code = status.HTTP_404_NOT_FOUND
#             raise response
#         return recipe
#
#     def get(self, request, pk):
#         recipe = self.get_object(pk)
#         if isinstance(recipe, Response):
#             return recipe
#         serializer = serializers.RecipeSerializer(instance=recipe, context={'request': request})
#         return Response(serializer.data)
#
#     def patch(self, request, pk):
#         recipe = self.get_object(pk)
#         if isinstance(recipe, Response):
#             return recipe
#         serializer = serializers.RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             partial=True,
#             context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
#
#     def delete(self, request, pk):
#         recipe = self.get_object(pk=pk)
#         if isinstance(recipe, Response):
#             return recipe
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# _--------------------------------------------------------------------------------------_
# class ApiRecipeList(ListCreateAPIView):
#     serializer_class = serializers.RecipeSerializer
#     queryset = models.Recipe.objects.all().select_related('author', 'category').prefetch_related('tags')
#     pagination_class = RecipePagination
#
#
# class ApiRecipeDetail(RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.RecipeSerializer
#     queryset = models.Recipe.objects.all().select_related('author', 'category').prefetch_related('tags')
#     pagination_class = RecipePagination

# _--------------------------------------------------------------------------------------_

class ApiRecipeViewSet(ModelViewSet):
    serializer_class = serializers.RecipeSerializer
    queryset = models.Recipe.objects.all().select_related('author', 'category').prefetch_related('tags')
    pagination_class = RecipePagination

    permission_classes = [IsAuthenticatedOrReadOnly]

    http_method_names = ['get', 'post', 'head', 'options', 'trace', 'patch', 'delete']

    def get_object(self):
        obj = self.get_queryset().filter(pk=self.kwargs.get('pk', '')).first()
        if not obj:
            response = APIException('Not found')
            response.status_code = status.HTTP_404_NOT_FOUND
            raise response

        self.check_object_permissions(self.request, obj)

        return obj

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PATCH']:
            return [permissions.IsOwner(),]
        return super().get_permissions()

# _--------------------------------------------------------------------------------------_

# @api_view(['GET', 'POST'])
# def api_recipe_list(request):
#
#     if request.method == 'POST':
#         serializer = serializers.RecipeSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
#
#     recipes = models.Recipe.objects.all().order_by('-created_at').order_by('-updated_at')
#     recipes = recipes.select_related('author', 'category').prefetch_related('tags')
#     serializer = serializers.RecipeSerializer(instance=recipes, many=True, context={'request': request})
#     return Response(serializer.data)


# @api_view(['GET', 'PATCH', 'DELETE'])
# def api_recipe_detail(request, pk=None):
#     if not pk:
#         return Response({'detail': 'Missing primary key'}, status=status.HTTP_400_BAD_REQUEST)
#
#     recipe = models.Recipe.objects.filter(
#         pk=pk
#     ).select_related('author', 'category').prefetch_related('tags').first()
#
#     if not recipe:
#         return Response({'detail': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'PATCH':
#         serializer = serializers.RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             partial=True,
#             context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     elif request.method == 'DELETE':
#         recipe.delete()
#         return Response({'detail': 'Recipe deleted'}, status=status.HTTP_200_OK)
#
#     serializer = serializers.RecipeSerializer(instance=recipe, context={'request': request})
#     return Response(serializer.data)


@api_view(['GET'])
def api_recipes_tag(request, pk=None):
    recipes = models.Recipe.objects.filter(tags__id=pk)
    recipes = recipes.select_related('author', 'category').prefetch_related('tags').first()
    serializer = serializers.RecipeSerializer(instance=recipes, context={'request': request})
    return Response(serializer.data)
