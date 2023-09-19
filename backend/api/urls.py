from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, UsersViewSet, RecipeViewSet, TagViewSet, FollowViewSet, ShoppingListAPIView, FollowCreateDestroyAPIView)

app_name = 'api'

router = DefaultRouter()
router.register('users/subscriptions', FollowViewSet, basename='subscriptions')
router.register('users', UsersViewSet)
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('users/<int:user_id>/subscribe/', FollowCreateDestroyAPIView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingListAPIView.as_view()),
    path('', include(router.urls)),
]
