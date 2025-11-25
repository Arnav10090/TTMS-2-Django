from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PTMSUser
from .serializers import (
    PTMSUserSerializer, PTMSUserCreateSerializer,
    PTMSTokenObtainPairSerializer, PTMSTokenRefreshSerializer,
    PTMSUserUpdateSerializer, PTMSChangePasswordSerializer
)
from .permissions import IsPTMSAuthenticated, IsPTMSAdmin


class PTMSTokenObtainPairView(TokenObtainPairView):
    """
    JWT token obtain endpoint for PTMS.
    Authenticates user with email and password.
    
    POST /auth/login/
    {
        "email": "user@example.com",
        "password": "password123"
    }
    
    Response:
    {
        "access": "eyJ...",
        "refresh": "eyJ..."
    }
    """
    serializer_class = PTMSTokenObtainPairSerializer
    permission_classes = [AllowAny]


class PTMSTokenRefreshView(TokenRefreshView):
    """
    JWT token refresh endpoint for PTMS.
    Refreshes expired access token using refresh token.
    
    POST /auth/refresh/
    {
        "refresh": "eyJ..."
    }
    
    Response:
    {
        "access": "eyJ..."
    }
    """
    serializer_class = PTMSTokenRefreshSerializer
    permission_classes = [AllowAny]


class PTMSUserViewSet(viewsets.ModelViewSet):
    """
    API endpoints for PTMS user management.
    
    Endpoints:
    - GET /auth/users/ - List users (admin only)
    - POST /auth/users/ - Create user
    - GET /auth/users/{id}/ - Get user details
    - PUT /auth/users/{id}/ - Update user
    - DELETE /auth/users/{id}/ - Delete user (admin only)
    - GET /auth/users/me/ - Get current user
    - POST /auth/users/me/update/ - Update current user
    - POST /auth/users/me/change-password/ - Change password
    - POST /auth/users/logout/ - Logout
    """
    queryset = PTMSUser.objects.all()
    permission_classes = [IsPTMSAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return PTMSUserCreateSerializer
        elif self.action in ['update', 'partial_update', 'update_profile']:
            return PTMSUserUpdateSerializer
        elif self.action == 'change_password':
            return PTMSChangePasswordSerializer
        return PTMSUserSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['destroy', 'list']:
            permission_classes = [IsPTMSAdmin]
        elif self.action in ['me', 'update_profile', 'change_password']:
            permission_classes = [IsPTMSAuthenticated]
        else:
            permission_classes = [IsPTMSAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """
        List all users (admin only).
        
        Query parameters:
        - role: Filter by role
        - is_active: Filter by active status
        - department: Filter by department
        """
        queryset = self.get_queryset()
        
        # Apply filters
        role = request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        department = request.query_params.get('department')
        if department:
            queryset = queryset.filter(department=department)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsPTMSAuthenticated])
    def me(self, request):
        """
        Get current authenticated user's profile.
        
        GET /auth/users/me/
        
        Response:
        {
            "id": 1,
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "role": "team_member",
            "department": "engineering",
            ...
        }
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsPTMSAuthenticated])
    def update_profile(self, request):
        """
        Update current user's profile.
        
        POST /auth/users/me/update/
        {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+1234567890"
        }
        """
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsPTMSAuthenticated])
    def change_password(self, request):
        """
        Change current user's password.
        
        POST /auth/users/me/change-password/
        {
            "old_password": "oldpassword123",
            "new_password": "newpassword123",
            "new_password_confirm": "newpassword123"
        }
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request.user)
            return Response(
                {'message': 'Password changed successfully.'},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[IsPTMSAuthenticated])
    def logout(self, request):
        """
        Logout user by blacklisting refresh token.
        
        POST /auth/users/logout/
        {
            "refresh": "eyJ..."
        }
        """
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {'message': 'Logout successful.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
