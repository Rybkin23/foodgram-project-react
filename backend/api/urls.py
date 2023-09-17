from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, UsersViewSet, RecipeViewSet, TagViewSet, FollowViewSet, ShoppingListAPIView

app_name = 'api'

router = DefaultRouter()
router.register('subscriptions', FollowViewSet)
router.register('users', UsersViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingListAPIView.as_view()),
    path('', include(router.urls)),
]
