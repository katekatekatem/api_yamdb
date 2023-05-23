from rest_framework import permissions


class IsAdminPermission(permissions.BasePermission):
    """Права для работы с пользователями."""

    def has_permission(self, request, _):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """Права для работы с отзывами и комментариями."""

    def has_permission(self, request, _):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )


class IsStaffOrAuthorOrReadOnlyPermission(permissions.BasePermission):
    """Права для работы с категориями и жанрами."""

    def has_permission(self, request, _):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, _, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
