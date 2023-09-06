from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, UsersViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]