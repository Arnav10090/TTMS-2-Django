from rest_framework import permissions


class IsTTMSAuthenticated(permissions.IsAuthenticated):
    """
    Permission to check if user is authenticated in TTMS.
    Extends REST framework's IsAuthenticated permission.
    """
    pass


class IsTTMSAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Permission to allow authenticated users full access.
    Unauthenticated users can only read.
    """
    pass


class IsTTMSOperator(permissions.BasePermission):
    """
    Permission to check if user is an TTMS Operator.
    Operators can view and manage vehicle data.
    """
    
    def has_permission(self, request, view):
        """Check if user is an operator."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'operator'
        )


class IsTTMSSupervisor(permissions.BasePermission):
    """
    Permission to check if user is an TTMS Supervisor.
    Supervisors can view, manage, and approve vehicle operations.
    """
    
    def has_permission(self, request, view):
        """Check if user is a supervisor."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['supervisor', 'manager', 'admin']
        )


class IsTTMSManager(permissions.BasePermission):
    """
    Permission to check if user is an TTMS Manager.
    Managers can view, manage, and generate reports.
    """
    
    def has_permission(self, request, view):
        """Check if user is a manager."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['manager', 'admin']
        )


class IsTTMSAdmin(permissions.BasePermission):
    """
    Permission to check if user is an TTMS Administrator.
    Admins have full access to TTMS system.
    """
    
    def has_permission(self, request, view):
        """Check if user is an admin."""
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsTTMSAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to allow admins full access.
    Others can only read.
    """
    
    def has_permission(self, request, view):
        """Allow read-only access to everyone, write access only to admins."""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_superuser)
        )


class HasFacilityAccess(permissions.BasePermission):
    """
    Permission to check if user has access to a specific facility.
    """
    
    def has_object_permission(self, request, view, obj):
        """Check if user has access to the facility."""
        # Check if object has facility_id attribute
        facility_id = getattr(obj, 'facility_id', None)
        
        if facility_id is None:
            return True
        
        return request.user.has_facility_access(facility_id)
