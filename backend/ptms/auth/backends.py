from django.contrib.auth.backends import ModelBackend
from .models import PTMSUser


class PTMSAuthBackend(ModelBackend):
    """
    Custom authentication backend for PTMS.
    
    Authenticates users by email and password.
    Independent from TTMS authentication.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate PTMS user.
        
        Supports authentication by:
        - Email (primary)
        - Username (fallback)
        
        Args:
            request: HTTP request
            username: Email or username
            password: User password
            **kwargs: Additional authentication parameters
            
        Returns:
            Authenticated PTMSUser or None
        """
        try:
            # Try to authenticate by email first
            user = PTMSUser.objects.get(email=username)
        except PTMSUser.DoesNotExist:
            try:
                # Fallback to username
                user = PTMSUser.objects.get(username=username)
            except PTMSUser.DoesNotExist:
                return None
        
        # Check password and user can authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Get PTMS user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            PTMSUser or None
        """
        try:
            return PTMSUser.objects.get(pk=user_id)
        except PTMSUser.DoesNotExist:
            return None
    
    def user_can_authenticate(self, user):
        """
        Check if user can be authenticated.
        
        Args:
            user: PTMSUser instance
            
        Returns:
            Boolean indicating if user can authenticate
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
