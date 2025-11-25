from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _


class PTMSUser(models.Model):
    """
    PTMS User Profile - extends Django's default User model.
    
    Provides PTMS-specific user attributes:
    - Role-based access control
    - Project assignment tracking
    - Department management
    - Session management
    """
    
    ROLE_CHOICES = [
        ('team_member', 'Team Member'),
        ('team_lead', 'Team Lead'),
        ('project_manager', 'Project Manager'),
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
    ]
    
    # Link to Django's built-in User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='ptms_profile',
        help_text='Link to Django User account'
    )
    
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
    
    class Meta:
        verbose_name = 'PTMS User Profile'
        verbose_name_plural = 'PTMS User Profiles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['department']),
            models.Index(fields=['employee_id']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"
    
    def has_department_access(self, department):
        """Check if user has access to specified department."""
        return self.department == department or self.user.is_superuser
    
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
        return self.role == 'admin' or self.user.is_superuser
