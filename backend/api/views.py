from django_filters.rest_framework import DjangoFilterBackend
from users.models import User
from recipes.models import (Tag, Ingredient, Recipe,
                            ShoppingList, Favorite, Follow)
from users.permissions import (IsAuthorOrReadOnly, AdminEditUsersPermission,
                               AdminOrReadOnly, IsAdminOwnerOrReadOnly)
from rest_framework import (filters, mixins, permissions, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from api.serializers import (IngredientSerializer, TagSerializer,
                             RecipeWriteSerializer, RecipeReadSerializer,
                             ShoppingListSerializer, FavoriteSerializer,
                             FollowSerializer)
from users.serializers import CustomUserSerializer
from .filters import RecipeFilter, IngredientSearchFilter


class UsersViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.order_by('pk')
    permission_classes = (AdminEditUsersPermission,)

    @action(
        methods=('GET', 'PATCH'), detail=False, url_path='me',
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
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(methods=['post'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = FavoriteSerializer(data=data,
                                        context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListViewSet(ModelViewSet):
    queryset = ShoppingList.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShoppingListSerializer


class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FollowSerializer
    pagination_class = LimitOffsetPagination
