from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from recipes import models, serializers


@api_view(['GET', 'POST'])
def api_recipe_list(request):

    if request.method == 'POST':
        serializer = serializers.RecipeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    recipes = models.Recipe.objects.all().order_by('-created_at').order_by('-updated_at')
    recipes = recipes.select_related('author', 'category').prefetch_related('tags')
    serializer = serializers.RecipeSerializer(instance=recipes, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET', 'PATCH', 'DELETE'])
def api_recipe_detail(request, pk=None):
    if not pk:
        return Response({'detail': 'Missing primary key'}, status=status.HTTP_400_BAD_REQUEST)

    recipe = models.Recipe.objects.filter(
        pk=pk
    ).select_related('author', 'category').prefetch_related('tags').first()

    if not recipe:
        return Response({'detail': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = serializers.RecipeSerializer(
            instance=recipe,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        recipe.delete()
        return Response({'detail': 'Recipe deleted'}, status=status.HTTP_200_OK)

    serializer = serializers.RecipeSerializer(instance=recipe, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def api_recipes_tag(request, pk=None):
    recipes = models.Recipe.objects.filter(tags__id=pk)
    recipes = recipes.select_related('author', 'category').prefetch_related('tags').first()
    serializer = serializers.RecipeSerializer(instance=recipes, context={'request': request})
    return Response(serializer.data)
