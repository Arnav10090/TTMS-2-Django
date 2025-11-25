from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TTMSUser


@admin.register(TTMSUser)
class TTMSUserAdmin(UserAdmin):
    """
    Custom admin interface for TTMS User model.
    Extends Django's UserAdmin with TTMS-specific fields.
    """
    
    model = TTMSUser
    
    # Define fieldsets for the admin change page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('TTMS Info', {'fields': ('role', 'facility_id', 'employee_id')}),
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
        ('TTMS Info', {'fields': ('role', 'facility_id')}),
    )
    
    # List display in admin list view
    list_display = ('email', 'first_name', 'last_name', 'role', 'facility_id', 'is_active', 'created_at')
    
    # Filters in admin list view
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'facility_id')
    
    # Search fields
    search_fields = ('email', 'first_name', 'last_name', 'employee_id', 'facility_id')
    
    # Ordering
    ordering = ('-created_at',)
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'last_login_at')
