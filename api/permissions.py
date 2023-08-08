from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Librarians").exists()


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Members").exists()
