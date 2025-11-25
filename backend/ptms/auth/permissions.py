from rest_framework import permissions


class IsPTMSAuthenticated(permissions.IsAuthenticated):
    """
    Permission to check if user is authenticated in PTMS.
    Extends REST framework's IsAuthenticated permission.
    """
    pass


class IsPTMSAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """
    Permission to allow authenticated users full access.
    Unauthenticated users can only read.
    """
    pass


class IsPTMSTeamMember(permissions.BasePermission):
    """
    Permission to check if user is a PTMS Team Member.
    Team members can view and contribute to tasks.
    """
    
    def has_permission(self, request, view):
        """Check if user is a team member."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == 'team_member'
        )


class IsPTMSTeamLead(permissions.BasePermission):
    """
    Permission to check if user is a PTMS Team Lead.
    Team leads can manage team tasks and workflows.
    """
    
    def has_permission(self, request, view):
        """Check if user is a team lead."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['team_lead', 'project_manager', 'admin']
        )


class IsPTMSProjectManager(permissions.BasePermission):
    """
    Permission to check if user is a PTMS Project Manager.
    Project managers can manage projects and teams.
    """
    
    def has_permission(self, request, view):
        """Check if user is a project manager."""
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in ['project_manager', 'admin']
        )


class IsPTMSAdmin(permissions.BasePermission):
    """
    Permission to check if user is a PTMS Administrator.
    Admins have full access to PTMS system.
    """
    
    def has_permission(self, request, view):
        """Check if user is an admin."""
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_superuser)
        )


class IsPTMSAdminOrReadOnly(permissions.BasePermission):
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


class HasDepartmentAccess(permissions.BasePermission):
    """
    Permission to check if user has access to a specific department.
    """
    
    def has_object_permission(self, request, view, obj):
        """Check if user has access to the department."""
        # Check if object has department attribute
        department = getattr(obj, 'department', None)
        
        if department is None:
            return True
        
        return request.user.has_department_access(department)
