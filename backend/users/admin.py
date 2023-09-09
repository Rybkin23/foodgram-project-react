from django.contrib import admin

from .forms import RecipeInLineFormSet
from .models import User
from recipes.models import (Favourite, Follow, Ingredient, Recipe,
                            RecipeIngredient, Tag, ShoppingList, RecipeTag)


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    pass


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    formset = RecipeInLineFormSet
    fields = ('ingredient', 'amount')
    readonly_fields = ('measurement_unit',)

    def measurement_unit(self, obj):
        return obj.Ingredient.measurement_unit
    measurement_unit.short_description = 'Единица измерения'

class RecipeTagInLine(admin.TabularInline):
    model = RecipeTag
    formset = RecipeInLineFormSet
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('admin_tag', 'author', 'name', 'cooking_time')
    list_filter = ('tags', 'author', 'name')
    search_fields = ('tags__name', 'author__username', 'name')
    inlines = (RecipeIngredientInLine, RecipeTagInLine)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    inlines = (RecipeTagInLine,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


@admin.register(Favourite, ShoppingList)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user',)
