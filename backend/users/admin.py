from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin


from .forms import RecipeInLineFormSet
from .models import User
from recipes.models import (
    Favorite, Follow, Ingredient, Recipe, RecipeIngredient,
    RecipeTag, ShoppingList, Tag)


@admin.register(User)
class UsersAdmin(ImportExportActionModelAdmin):
    list_display = ('id', 'first_name', 'email')
    list_filter = ('first_name', 'email')
    search_fields = list_filter
    list_per_page = 10


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    formset = RecipeInLineFormSet
    fields = ('ingredient', 'amount')
    readonly_fields = ('measurement_unit',)

    def measurement_unit(self, obj):
        return obj.ingredient.measurement_unit
    measurement_unit.short_description = 'Единица измерения'


class RecipeTagInLine(admin.TabularInline):
    model = RecipeTag
    formset = RecipeInLineFormSet
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'get_favorite_count', 'admin_tag',
                    'author', 'cooking_time')
    list_filter = ('tags', 'author', 'name')
    search_fields = ('tags__name', 'author__username', 'name')
    inlines = (RecipeIngredientInLine, RecipeTagInLine)
    list_per_page = 10

    def get_favorite_count(self, obj):
        return obj.in_favorites.count()

    get_favorite_count.short_description = 'Добавлено в избранное'

    def before_import_row(self, row, **kwargs):
        recipe_amount = row.get('amount')
        if recipe_amount:
            self.amount = recipe_amount

    def after_import_instance(self, instance, new, row_number=None, **kwargs):
        recipe_ingredient = instance.recipeingredient_set.first()
        if recipe_ingredient:
            recipe_ingredient.amount = instance.amount
            recipe_ingredient.save()

    def after_import(self, dataset, result, **kwargs):
        Recipe.objects.update(amount=None)


@admin.register(Tag)
class TagAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_per_page = 10


@admin.register(Ingredient)
class IngredientAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_per_page = 10


@admin.register(Favorite, ShoppingList)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'get_tags', 'user')
    list_filter = ('recipe__tags__name', 'user')
    search_fields = ('recipe', 'user')
    list_per_page = 10

    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.recipe.tags.all()])

    get_tags.short_description = 'Тэги'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user',)
    list_per_page = 10
