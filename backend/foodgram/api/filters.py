from django_filters.rest_framework import (BooleanFilter, CharFilter,
                                           FilterSet, ModelChoiceFilter,
                                           ModelMultipleChoiceFilter)

from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class TagFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if bool(value) and not self.request.user.is_anonymous:
            return queryset.filter(favoriterecipes__user=self.request.user)
        return queryset.exclude(favoriterecipes__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        if bool(value) and not self.request.user.is_anonymous:
            return queryset.filter(shoppingcarts__user=self.request.user)
        return queryset.exclude(shoppingcarts__user=self.request.user)
