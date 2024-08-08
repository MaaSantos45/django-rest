from rest_framework import serializers

from recipes.models import Category, Recipe
from django.contrib.auth.models import User
from collections import defaultdict
from recipes.validators import RecipeValidator

from tags.models import Tag


# class TagSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     slug = serializers.SlugField()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        # fields = '__all__'
        fields = ['id', 'name', 'slug']

# class RecipeSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     slug = serializers.SlugField()
#     public = serializers.BooleanField(source='is_published')
#     preparation = serializers.SerializerMethodField()
#     category = serializers.StringRelatedField()
#     author = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(),
#     )
#     tags = TagSerializer(many=True)
#     tag_links = serializers.HyperlinkedRelatedField(
#         many=True,
#         source='tags',
#         queryset=Tag.objects.all(),
#         view_name='recipes:api_recipes_tag',
#     )
#
#     @staticmethod
#     def get_preparation(recipe):
#         return f"{recipe.preparation_time} {recipe.preparation_time_unit}"


class RecipeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self._json_erros = defaultdict(list)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'slug',
            'public',
            'preparation',
            'preparation_time',
            'preparation_time_unit',
            'preparation_steps',
            'servings',
            'servings_unit',
            'author',
            'category',
            'tags',
            'tag_links',
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)

    category = serializers.StringRelatedField()

    tags = TagSerializer(many=True, required=False)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:api_recipes_tag',
        read_only=True
    )

    @staticmethod
    def get_preparation(recipe):
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    def validate(self, attrs):
        if self.instance is not None:
            for key, value in self.instance.__dict__.items():
                if key not in attrs and not key.startswith('_'):
                    attrs[key] = value

        data = attrs
        RecipeValidator(data, error_class=serializers.ValidationError)
        return super().validate(attrs)
