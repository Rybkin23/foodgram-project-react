from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Теги"""
    name = models.CharField(
        verbose_name='Название тэга',
        max_length=200,
        null=True,
        blank=False)
    color = models.CharField(
        max_length=7, default="#ffffff", null=True, blank=True)
    slug = models.CharField(
        max_length=200, null=True, blank=True,
        validators=[RegexValidator(
            regex='^[-a-zA-Z0-9_]+$',
            message='Введите допустимое значение',)])


class Ingredient(models.Model):
    """Ингредиенты"""
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
        blank=False)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
        blank=False)


class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        null=True,
        blank=False)
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=False)
    text = models.TextField(null=True,)
    cooking_time = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(1)])
    tags = models.ForeignKey(
        Tag, on_delete=models.CASCADE, null=True, related_name='tags')
    ingredients = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, null=True, related_name='Ingredients')


class ShoppingList(models.Model):
    """Список покупок"""
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='buyer')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipes_list')


class Favourite(models.Model):
    """Избранное"""
    fan = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='fan')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='fan_recipes')


class Follow(models.Model):  # page, limit, recipes_limit
    """Подписка"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        unique_together = ('user', 'following')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
