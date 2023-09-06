<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from users.models import User
from recipes.models import Tag, Ingredient, Recipe, ShoppingList, Favourite, Follow
from users.permissions import IsAuthorOrReadOnly, AdminEditUsersPermission, AdminOrReadOnly, IsAdminOwnerOrReadOnly
from rest_framework import (filters, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from api.serializers import (IngredientSerializer, TagSerializer,
                             RecipeReadSerializer, RecipeWriteSerializer,
                             ShoppingListSerializer, FavouriteSerializer,
                             FollowSerializer, UserSerializer)


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.order_by('pk')
    permission_classes = (AdminEditUsersPermission,)

    @action(
        methods=['GET', 'PATCH'], detail=False, url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_update_me(self, request):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if self.request.method == 'PATCH':
            serializer.validated_data.pop('role', None)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)
    search_fields = ('^name',)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)

    if action in ['list', 'retrieve']:
        serializer_class = RecipeReadSerializer
    else:
        serializer_class = RecipeWriteSerializer

    @action(detail=True, methods=['get'])
    def is_favorited(self, request, pk=None):
        recipe = self.get_object()
        is_favorited = recipe.favorite.filter(id=request.user.id).exists()
        return Response({'is_favorited': int(is_favorited)})

    @action(detail=True, methods=['get'])
    def is_in_shopping_cart(self, request, pk=None):
        recipe = self.get_object()
        is_in_shopping_cart = recipe.shopping_cart.filter(id=request.user.id).exists()
        return Response({'is_in_shopping_cart': int(is_in_shopping_cart)})


class ShoppingListViewSet(ModelViewSet):
    queryset = ShoppingList.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShoppingListSerializer


class FavouriteViewSet(ModelViewSet):
    queryset = Favourite.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavouriteSerializer


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
>>>>>>> 87ae675 (Закончил тэги)
