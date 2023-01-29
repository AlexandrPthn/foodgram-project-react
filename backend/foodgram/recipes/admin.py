from django.contrib import admin

from .models import (Ingredient, Tag, Recipe, IngredientsRecipe,
                     Follow, FavoriteRecipe)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'text',
        'cooking_time'
    )
    list_filter = ('name', 'author')


@admin.register(IngredientsRecipe)
class IngredientsRecipeAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
