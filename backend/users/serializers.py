from django.db import models
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import User


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',)  # "is_subscribed"


class CustomUserCreateSerializer(UserCreateSerializer):

    password = models.CharField(
        verbose_name='Пароль',
        help_text='Введите пароль',
        max_length=150,
        blank=False)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password',)
