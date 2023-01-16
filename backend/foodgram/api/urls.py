from django.urls import include, path
from rest_framework import routers

from .views import (TagViewSet, IngredientViewSet, RecipeViewSet, IngredientsRecipeViewSet)

router = routers.DefaultRouter()

router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'recipesIn', IngredientsRecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
