from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):

    def has_permission(self, request, view):
        return request.user == view.get_object()


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderator").exists()
