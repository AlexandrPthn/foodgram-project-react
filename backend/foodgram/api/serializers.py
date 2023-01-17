from django.core.exceptions import ValidationError
from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, IngredientsRecipe
from users.models import CustomUser
from drf_extra_fields.fields import Base64ImageField


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsRecipeSerializer(many=True,
                                              source='ingredientsrecipe_set',
                                              read_only=True
                                              )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def create(self, validated_data):
        image = validated_data.pop('image')

        recipe = Recipe.objects.create(image=image,
                                       author=self.context['request'].user,
                                       **validated_data)

        tags = self.initial_data.get('tags')
        recipe.tags.set(tags)
        
        ingredients_data = self.initial_data.get('ingredients')
        for ingredient in ingredients_data:
            ingredient_id = Ingredient.objects.get(id=ingredient.get('id'))
            ingredient_amount = ingredient.get('amount')
            IngredientsRecipe.objects.create(ingredient=ingredient_id,
                                             recipe=recipe,
                                             amount=ingredient_amount
                                             )
        return recipe
    
    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        instance.save()
        IngredientsRecipe.objects.filter(recipe=instance).delete()
        ingredients_data = self.initial_data.get('ingredients')
        for ingredient in ingredients_data:
            ingredient_id = Ingredient.objects.get(id=ingredient.get('id'))
            ingredient_amount = ingredient.get('amount')
            IngredientsRecipe.objects.create(ingredient=ingredient_id,
                                             recipe=instance,
                                             amount=ingredient_amount
                                             )
        return instance


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientsRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')
