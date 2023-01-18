from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from recipes.models import Tag, Ingredient, Recipe, Follow, FavoriteRecipe
from users.models import CustomUser
from .serializers import (CustomUserSerializer, TagSerializer,
                          IngredientSerializer, RecipeSerializer,
                          FollowSerializer, FavoriteRecipeSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    additional_serializer = FollowSerializer

    @action(methods=['GET'], detail=False, url_path='me')
    def get_current_user_info(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False)
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        serializer = self.additional_serializer(queryset,
                                                many=True,
                                                context={'request': request})
        return Response(serializer.data)

    @action(methods=['POST', 'DELETE'], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        author = get_object_or_404(CustomUser, id=kwargs.get('pk'))
        if request.method == 'POST':
            if user == author:
                return Response(
                    {'errors': 'Вы не можете подписываться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST)
            if Follow.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного пользователя'},
                    status=status.HTTP_400_BAD_REQUEST)
            subscribe = Follow.objects.create(user=user, author=author)
            serializer = self.additional_serializer(
                subscribe,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if user == author:
                return Response(
                    {'errors': 'Имена пользователя и автора совпадают'},
                    status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.filter(user=user, author=author)
            if follow.exists():
                follow.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'У вас нет подписки на такого автора'},
                status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, **kwargs):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
            if FavoriteRecipe.objects.filter(recipe=recipe,
                                             user=request.user).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            instance = FavoriteRecipe.objects.create(user=request.user,
                                                     recipe=recipe)
            serializer = FavoriteRecipeSerializer(
                instance,
                context={'request': request})
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=kwargs.get('pk'))
            if FavoriteRecipe.objects.filter(user=request.user,
                                             recipe=recipe).exists():
                FavoriteRecipe.objects.filter(user=request.user,
                                              recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
