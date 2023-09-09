from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Теги"""
    name = models.CharField(
<<<<<<< HEAD
        verbose_name='Название тэга',
        max_length=200,
        null=True,
        blank=False)
    color = models.CharField(
        max_length=7, default="#ffffff", null=True, blank=True)
    slug = models.CharField(
        max_length=200, null=True, blank=True,
=======
        verbose_name='Название', max_length=200, null=True, blank=False,
        unique=True)
    color = models.CharField(
        max_length=7, default="#ffffff", null=True,
        blank=True, unique=True, verbose_name='Цвет')
    slug = models.SlugField(
        max_length=200, null=True, blank=True,
        unique=True, verbose_name='Слаг',
>>>>>>> 1688454 (Закончил админку, но есть один косяк)
        validators=[RegexValidator(
            regex='^[-a-zA-Z0-9_]+$',
            message='Введите допустимое значение',)])

<<<<<<< HEAD
=======
    class Meta:
        verbose_name_plural = 'Тэг'
        verbose_name = 'Тэги'

    def __str__(self):
        return self.name

>>>>>>> 87ae675 (Закончил тэги)

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

<<<<<<< HEAD
=======
    class Meta:
        verbose_name_plural = 'Ингредиент'
        verbose_name = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name

>>>>>>> 87ae675 (Закончил тэги)

class Recipe(models.Model):
    """Рецепты"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор')
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        null=True,
        blank=False)
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=False, verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание рецепта', null=True)
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, м', default=0,
        validators=[MinValueValidator(1)])
<<<<<<< HEAD
    tags = models.ManyToManyField(Tag, related_name='recipes')
<<<<<<< HEAD
    ingredients = models.ForeignKey(
<<<<<<< HEAD
        Ingredient, on_delete=models.CASCADE, null=True, related_name='Ingredients')
=======
        Ingredient, on_delete=models.CASCADE, null=True)
=======
=======
    tags = models.ManyToManyField(
        Tag, related_name='recipes', through='RecipeTag', verbose_name='Тэг')
>>>>>>> 1688454 (Закончил админку, но есть один косяк)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
>>>>>>> f4dd0b4 (переписал некоторые модели)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Рецепт'
        verbose_name = 'Рецепты'

    def __str__(self):
        return self.name
>>>>>>> 87ae675 (Закончил тэги)

    def admin_tag(self):
        return ', '.join([tag.name for tag in self.tags.all()])
    admin_tag.short_description = 'Тэг'


class RecipeTag(models.Model):
    """Модель связи добавления и контроля тегов"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')

    class Meta:
        unique_together = ('tag', 'recipe')
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги рецепта'


class RecipeIngredient(models.Model):
    """Добавление количества для ингредиента"""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   null=True, related_name='recipes', verbose_name='Ингредиент')
    amount = models.FloatField(validators=[MinValueValidator(1)], verbose_name='Количество')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               null=True)

    def measurement_unit(self):
        return self.ingredient.measurement_unit

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class ShoppingList(models.Model):
    """Список покупок"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shoplist')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shoplist')

    class Meta:
        verbose_name_plural = 'Список покупок'
        verbose_name = 'Списки покупок'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Favourite(models.Model):
    """Избранное"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favourites')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favourites')

    class Meta:
        verbose_name_plural = 'Избранный рецепт'
        verbose_name = 'Избранные рецепты'
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Follow(models.Model):
    """Подписка"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', verbose_name='Автор')

    class Meta:
        unique_together = ('user', 'author')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
