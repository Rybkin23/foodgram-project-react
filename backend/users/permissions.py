from rest_framework.permissions import BasePermission, SAFE_METHODS

# Гость, авторизованный пользователь, автор, администратор
class IsAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or obj.author == request.user)


class AdminEditUsersPermission(BasePermission):
    """Работать с пользователями могут только админы."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class AdminOrReadOnly(BasePermission):
    """Изменять может админ, остальные только читать."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOwnerOrReadOnly(BasePermission):
    """Админ или автор остальные только чтение."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or obj.author == request.user)
