from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PTMSUser


@admin.register(PTMSUser)
class PTMSUserAdmin(UserAdmin):
    """
    Custom admin interface for PTMS User model.
    Extends Django's UserAdmin with PTMS-specific fields.
    """
    
    model = PTMSUser
    
    # Define fieldsets for the admin change page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('PTMS Info', {'fields': ('role', 'department', 'employee_id', 'last_project_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'last_login_at', 'created_at', 'updated_at')}),
    )
    
    # Define fieldsets for the admin add page
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('PTMS Info', {'fields': ('role', 'department')}),
    )
    
    # List display in admin list view
    list_display = ('email', 'first_name', 'last_name', 'role', 'department', 'is_active', 'created_at')
    
    # Filters in admin list view
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'department')
    
    # Search fields
    search_fields = ('email', 'first_name', 'last_name', 'employee_id', 'department')
    
    # Ordering
    ordering = ('-created_at',)
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'last_login_at')
