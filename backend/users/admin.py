from django.contrib import admin

from .models import User
from recipes.models import (Tag, Ingredient, Recipe,
                            ShoppingList, Favourite, Follow)


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(ShoppingList)
admin.site.register(Favourite)
admin.site.register(Follow)
