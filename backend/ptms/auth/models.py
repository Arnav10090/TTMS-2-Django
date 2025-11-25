from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class PTMSUserManager(BaseUserManager):
    """
    Custom manager for PTMS User model.
    Handles user creation with email as the primary identifier.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular PTMS user."""
        if not email:
            raise ValueError(_('The Email field must be set.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser for PTMS."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class PTMSUser(AbstractUser):
    """
    Custom User model for PTMS application.
    
    Extends Django's AbstractUser to provide:
    - Email-based authentication
    - Role-based access control
    - Project assignment tracking
    - Session management
    
    Independent from TTMS User model.
    """
    
    ROLE_CHOICES = [
        ('team_member', 'Team Member'),
        ('team_lead', 'Team Lead'),
        ('project_manager', 'Project Manager'),
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
        help_text='User role in PTMS system'
    )
    department = models.CharField(
        max_length=100,
        blank=True,
        help_text='User department'
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
    last_project_id = models.IntegerField(
        blank=True,
        null=True,
        help_text='Last project the user accessed'
    )
    last_login_at = models.DateTimeField(
        auto_now=True,
        help_text='Last login timestamp'
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = PTMSUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = 'PTMS User'
        verbose_name_plural = 'PTMS Users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['department']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def has_department_access(self, department):
        """Check if user has access to specified department."""
        return self.department == department or self.is_superuser
    
    def is_team_member(self):
        """Check if user is a team member."""
        return self.role == 'team_member'
    
    def is_team_lead(self):
        """Check if user is a team lead."""
        return self.role == 'team_lead'
    
    def is_project_manager(self):
        """Check if user is a project manager."""
        return self.role == 'project_manager'
    
    def is_admin_role(self):
        """Check if user is an admin."""
        return self.role == 'admin' or self.is_superuser
