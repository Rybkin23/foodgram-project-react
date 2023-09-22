import logging

from django.core.files.base import ContentFile
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    FavoriteSerializer, FollowSerializer, IngredientSerializer,
    RecipeIngredientReadSerializer, RecipeReadSerializer,
    RecipeWriteSerializer, ShoppingListSerializer, TagSerializer)
from recipes.models import (
    Favorite, Follow, Ingredient, Recipe, RecipeIngredient, ShoppingList, Tag)
from users.models import User
from users.permissions import IsAuthorOrReadOnly
from users.serializers import CustomUserSerializer
from .filters import IngredientSearchFilter, RecipeFilter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UsersViewSet(ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.order_by('pk')
    permission_classes = (IsAuthorOrReadOnly,)

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
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if (not ShoppingList.objects.filter(
                user=request.user, recipe=recipe).exists()):
            ShoppingList.objects.create(user=request.user, recipe=recipe)
            serializer = ShoppingListSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_list_item = get_object_or_404(
            ShoppingList, user=request.user, recipe=recipe)
        shopping_list_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)


class FollowCreateDestroyAPIView(APIView):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        user = request.user
        if not Follow.objects.filter(user=user, author=author).exists():
            Follow.objects.create(user=user, author=author)
            return Response(self.serializer_class(
                author, context={'request': request}).data,
                status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        author = get_object_or_404(User, id=self.kwargs.get('user_id'))
        follow = get_object_or_404(Follow, user=request.user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoadShopListAPIView(APIView):
    serializer_class = RecipeIngredientReadSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__recipeshoplist__user=request.user).values_list(
                'ingredient__name', 'ingredient__measurement_unit').annotate(
                    amount=Sum('amount'))
        shop_list = '\n'.join([
            f'{ingredient[0]} - {ingredient[2]} {ingredient[1]}'
            for ingredient in ingredients])
        filename = 'shop_list.txt'
        content_file = ContentFile(shop_list)
        response = HttpResponse(content_file, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
