from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения ингредиента',
        max_length=50
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
        CustomUser,
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
        verbose_name='Тэги рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )
    
    class Meta:
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
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Ингредиент в рецептах'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'Ингредиент: {self.ingredient} (Рецепт: {self.recipe})'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="following"
    )

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Автор'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
        ordering = ['user']

    def __str__(self):
        return self.user.username
