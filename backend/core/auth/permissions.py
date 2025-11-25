from rest_framework import permissions


class IsAuthenticated(permissions.IsAuthenticated):
    """
    Custom IsAuthenticated permission for both TTMS and PTMS
    """
    pass


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Allow authenticated users to perform all operations.
    Allow unauthenticated users to read-only.
    """
    pass


class IsTTMSAdmin(permissions.BasePermission):
    """
    Permission to check if user is admin for TTMS app
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsPTMSAdmin(permissions.BasePermission):
    """
    Permission to check if user is admin for PTMS app
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
