from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from .models import TTMSUser


class TTMSAuthBackend(ModelBackend):
    """
    Custom authentication backend for TTMS.
    
    Authenticates users by email and password.
    Independent from PTMS authentication.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate TTMS user.
        
        Supports authentication by:
        - Email (primary)
        - Username (fallback)
        
        Args:
            request: HTTP request
            username: Email or username
            password: User password
            **kwargs: Additional authentication parameters
            
        Returns:
            Authenticated TTMSUser or None
        """
        try:
            # Try to authenticate by email first
            user = TTMSUser.objects.get(email=username)
        except TTMSUser.DoesNotExist:
            try:
                # Fallback to username
                user = TTMSUser.objects.get(username=username)
            except TTMSUser.DoesNotExist:
                return None
        
        # Check password and user can authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Get TTMS user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            TTMSUser or None
        """
        try:
            return TTMSUser.objects.get(pk=user_id)
        except TTMSUser.DoesNotExist:
            return None
    
    def user_can_authenticate(self, user):
        """
        Check if user can be authenticated.
        
        Args:
            user: TTMSUser instance
            
        Returns:
            Boolean indicating if user can authenticate
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
