from django_filters.rest_framework import DjangoFilterBackend
from users.models import User
from recipes.models import (Tag, Ingredient, Recipe,
                            ShoppingList, Favorite, Follow)
from users.permissions import IsAuthorOrReadOnly
from rest_framework import (filters, mixins, permissions, status,
                            viewsets)
import logging
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from api.serializers import (IngredientSerializer, TagSerializer,
                             RecipeWriteSerializer, RecipeReadSerializer,
                             ShoppingListSerializer, FavoriteSerializer,
                             FollowSerializer)
from users.serializers import CustomUserSerializer
from .filters import RecipeFilter, IngredientSearchFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UsersViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.order_by('pk')
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

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
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthorOrReadOnly,)
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


class ShoppingListAPIView(APIView):
    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        ShoppingList.objects.create(user=request.user, recipe=recipe)
        serializer = ShoppingListSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = Recipe.objects.get(id=recipe_id)
        ShoppingList.objects.filter(user=request.user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(following__user=user)
        # logger.info('Queryset: %s', queryset)
        return queryset


class FollowCreateDestroyAPIView(APIView):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = LimitOffsetPagination

    def post(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        user = request.user
        Follow.objects.create(user=user, author=author)
        return Response(self.serializer_class(
            author, context={'request': request}).data,
            status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        follow = author.following.filter(user=request.user)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
