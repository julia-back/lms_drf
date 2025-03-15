from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    """
    Класс разрешения. Проверяет, что текущий авторизованный пользователь
    запрашивает свой объект модели пользователя.
    """

    def has_permission(self, request, view):
        return request.user == view.get_object()


class IsModerator(BasePermission):
    """класс разрешения. Проверяет, что текущий авторизованный пользователь входит в группу модераторов."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderator").exists()
