from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, data):
        user = self.context['request'].user.id
        return data.following.filter(user=user).exists()
