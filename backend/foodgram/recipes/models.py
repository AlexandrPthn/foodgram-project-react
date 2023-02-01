from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения ингредиента',
        max_length=20
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        unique=True
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=50,
        unique=True
    )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=50,
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэг'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
        help_text="Автор публикации"
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
        blank=True,
        help_text='Загрузите картинку рецепта'
    )
    text = models.TextField(
        verbose_name="Описание рецепта",
        help_text="Описание рецепта"
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты рецепта',
        through='IngredientsRecipe',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Наименование ингредиента',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Наименование рецепта',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1, message='Минимальное количество 1!')]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецептах'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            UniqueConstraint(fields=['ingredient', 'recipe'],
                             name='unique_recipe')
        ]

    def __str__(self):
        return f'Ингредиент: {self.ingredient} (Рецепт: {self.recipe})'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'
        constraints = [
            UniqueConstraint(fields=['user', 'author'],
                             name='unique_follow')
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoriterecipes',
        verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favoriterecipes',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favorite')
        ]

    def __str__(self):
        return self.user.username


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcarts',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping')
        ]

    def __str__(self):
        return (f'Список покупок пользователя {self.user.username}')
