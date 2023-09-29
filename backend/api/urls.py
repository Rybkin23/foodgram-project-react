from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FavoriteChangeAPIView, FollowCreateDestroyAPIView, FollowViewSet,
    IngredientViewSet, LoadShopListAPIView, RecipeViewSet,
    ShoppingListChangeAPIView, TagViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users/subscriptions', FollowViewSet, basename='subscriptions')
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('users/<int:user_id>/subscribe/',
         FollowCreateDestroyAPIView.as_view()),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteChangeAPIView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingListChangeAPIView.as_view()),
    path('recipes/download_shopping_cart/', LoadShopListAPIView.as_view()),
    path('', include(router.urls)),
]
