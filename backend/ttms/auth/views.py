from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import TTMSUser
from .serializers import (
    TTMSUserSerializer, TTMSUserCreateSerializer,
    TTMSTokenObtainPairSerializer, TTMSTokenRefreshSerializer,
    TTMSUserUpdateSerializer, TTMSChangePasswordSerializer
)
from .permissions import IsTTMSAuthenticated, IsTTMSAdmin


class TTMSTokenObtainPairView(TokenObtainPairView):
    """
    JWT token obtain endpoint for TTMS.
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
    serializer_class = TTMSTokenObtainPairSerializer
    permission_classes = [AllowAny]


class TTMSTokenRefreshView(TokenRefreshView):
    """
    JWT token refresh endpoint for TTMS.
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
    serializer_class = TTMSTokenRefreshSerializer
    permission_classes = [AllowAny]


class TTMSUserViewSet(viewsets.ModelViewSet):
    """
    API endpoints for TTMS user management.
    
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
    queryset = TTMSUser.objects.all()
    permission_classes = [IsTTMSAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return TTMSUserCreateSerializer
        elif self.action in ['update', 'partial_update', 'update_profile']:
            return TTMSUserUpdateSerializer
        elif self.action == 'change_password':
            return TTMSChangePasswordSerializer
        return TTMSUserSerializer
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['destroy', 'list']:
            permission_classes = [IsTTMSAdmin]
        elif self.action in ['me', 'update_profile', 'change_password']:
            permission_classes = [IsTTMSAuthenticated]
        else:
            permission_classes = [IsTTMSAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def list(self, request, *args, **kwargs):
        """
        List all users (admin only).
        
        Query parameters:
        - role: Filter by role
        - is_active: Filter by active status
        - facility_id: Filter by facility
        """
        queryset = self.get_queryset()
        
        # Apply filters
        role = request.query_params.get('role')
        if role:
            queryset = queryset.filter(role=role)
        
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        facility_id = request.query_params.get('facility_id')
        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsTTMSAuthenticated])
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
            "role": "operator",
            "facility_id": "facility-1",
            ...
        }
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsTTMSAuthenticated])
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
    
    @action(detail=False, methods=['post'], permission_classes=[IsTTMSAuthenticated])
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
    
    @action(detail=False, methods=['post'], permission_classes=[IsTTMSAuthenticated])
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
