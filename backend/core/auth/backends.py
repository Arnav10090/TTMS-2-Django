from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class CustomAuthBackend(ModelBackend):
    """Custom authentication backend for TTMS and PTMS"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate user with username and password.
        Supports both username and email as username parameter.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                return None
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
