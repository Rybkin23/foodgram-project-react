from djoser.views import UserViewSet

from .serializers import CustomUserCreateSerializer


class CustomUserCreateViewSet(UserViewSet):
    serializer_class = CustomUserCreateSerializer
