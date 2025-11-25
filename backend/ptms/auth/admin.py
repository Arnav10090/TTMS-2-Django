from django.contrib import admin
from .models import PTMSUser


@admin.register(PTMSUser)
class PTMSUserAdmin(admin.ModelAdmin):
    """
    Admin interface for PTMS User Profile model.
    Manages PTMS-specific user attributes and roles.
    """
    
    model = PTMSUser
    
    # Define fieldsets for the admin change page
    fieldsets = (
        ('User Account', {'fields': ('user',)}),
        ('PTMS Info', {'fields': ('role', 'department', 'employee_id', 'last_project_id')}),
        ('Contact', {'fields': ('phone_number',)}),
        ('Important dates', {'fields': ('last_login_at', 'created_at', 'updated_at')}),
    )
    
    # List display in admin list view
    list_display = ('__str__', 'role', 'department', 'employee_id', 'created_at')
    
    # Filters in admin list view
    list_filter = ('role', 'department', 'created_at')
    
    # Search fields
    search_fields = ('user__username', 'user__email', 'employee_id', 'department')
    
    # Ordering
    ordering = ('-created_at',)
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'last_login_at')

