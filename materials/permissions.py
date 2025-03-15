from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Класс разрешения, проверяющий, является ли текущий авторизованный
    пользователь владельцем по полю owner.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
