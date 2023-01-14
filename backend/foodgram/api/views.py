from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Tag, Ingredient, Recipe
from users.models import CustomUser
from .serializers import (CustomUserSerializer, TagSerializer,
                          IngredientSerializer, RecipeSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
 
    @action(
        methods=['GET'],
        detail=False,
        url_path='me')
    def get_current_user_info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
