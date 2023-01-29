from django.urls import include, path
from rest_framework import routers

from .views import (TagViewSet, IngredientViewSet, RecipeViewSet)
from api.views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
