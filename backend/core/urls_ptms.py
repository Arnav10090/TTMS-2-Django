"""
PTMS (Project Task Management System) URL Configuration

This is the main URL router for the PTMS application.
All PTMS API endpoints are defined here.

Routes:
- /admin/ - Django admin interface
- /api/ptms/ - PTMS data endpoints (projects, tasks, etc.)
- /api/ptms/auth/ - PTMS authentication endpoints
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenVerifyView

# Import PTMS auth views and viewsets
from ptms.auth.views import (
    PTMSTokenObtainPairView,
    PTMSTokenRefreshView,
    PTMSUserViewSet
)

# Import PTMS data viewsets
from ptms.views import (
    ProjectViewSet,
    TaskViewSet
)

# Create router for PTMS endpoints
router = DefaultRouter()

# Auth routes
router.register(r'auth/users', PTMSUserViewSet, basename='ptms-users')

# Data routes
router.register(r'projects', ProjectViewSet, basename='ptms-project')
router.register(r'tasks', TaskViewSet, basename='ptms-task')

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints with PTMS router
    path('api/ptms/', include(router.urls)),
    
    # JWT Token endpoints
    path('api/ptms/auth/login/', PTMSTokenObtainPairView.as_view(), name='ptms-token-obtain-pair'),
    path('api/ptms/auth/refresh/', PTMSTokenRefreshView.as_view(), name='ptms-token-refresh'),
    path('api/ptms/auth/verify/', TokenVerifyView.as_view(), name='ptms-token-verify'),
]
