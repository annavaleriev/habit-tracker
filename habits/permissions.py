from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Класс для проверки прав доступа к объекту"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Если метод запроса входит в список безопасных методов
            return True
        return obj.owner == request.user
