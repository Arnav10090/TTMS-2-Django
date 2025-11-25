from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class TTMSUserManager(BaseUserManager):
    """
    Custom manager for TTMS User model.
    Handles user creation with email as the primary identifier.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular TTMS user."""
        if not email:
            raise ValueError(_('The Email field must be set.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser for TTMS."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class TTMSUser(AbstractUser):
    """
    Custom User model for TTMS application.
    
    Extends Django's AbstractUser to provide:
    - Email-based authentication
    - Role-based access control
    - Facility assignment tracking
    - Session management
    
    Independent from PTMS User model.
    """
    
    ROLE_CHOICES = [
        ('operator', 'Operator'),
        ('supervisor', 'Supervisor'),
        ('manager', 'Manager'),
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
    ]
    
    # Email as unique identifier
    email = models.EmailField(_('email address'), unique=True, validators=[EmailValidator()])
    
    # User metadata
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer',
        help_text='User role in TTMS system'
    )
    facility_id = models.CharField(
        max_length=100,
        blank=True,
        help_text='Associated facility identifier'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text='User contact number'
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text='Employee identification number'
    )
    
    # Status tracking
    is_active = models.BooleanField(
        default=True,
        help_text='Whether user can log in'
    )
    last_login_facility = models.CharField(
        max_length=100,
        blank=True,
        help_text='Last facility the user accessed'
    )
    last_login_at = models.DateTimeField(
        auto_now=True,
        help_text='Last login timestamp'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = TTMSUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'TTMS User'
        verbose_name_plural = 'TTMS Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['facility_id']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def has_facility_access(self, facility_id):
        """Check if user has access to specified facility."""
        return self.facility_id == facility_id or self.is_superuser
    
    def is_operator(self):
        """Check if user is an operator."""
        return self.role == 'operator'
    
    def is_supervisor(self):
        """Check if user is a supervisor."""
        return self.role == 'supervisor'
    
    def is_manager(self):
        """Check if user is a manager."""
        return self.role == 'manager'
    
    def is_admin_role(self):
        """Check if user is an admin."""
        return self.role == 'admin' or self.is_superuser
