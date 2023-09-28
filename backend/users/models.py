from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Пользователь"""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    email = models.EmailField(
        verbose_name='Электронная почта',
        help_text='Введите почту',
        max_length=254,
        unique=True, blank=False)

    username = models.CharField(
        verbose_name='Логин',
        help_text='Введите логин',
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex='^[\w.@+-]+',
            message='Введите допустимое значение',)])

    first_name = models.CharField(
        verbose_name='Имя',
        help_text='Введите имя',
        max_length=150,
        blank=False)

    last_name = models.CharField(
        verbose_name='Фамилия',
        help_text='Введите фамилию',
        max_length=150,
        blank=False)

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username
