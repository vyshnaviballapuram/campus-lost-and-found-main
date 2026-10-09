"""
Admin configuration for Items app.
Yeh file Django admin panel ki settings define karti hai.
"""

from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Item model ke liye admin configuration.
    Admin panel mein items ko manage karne ke liye.
    """
    
    # List view mein dikhne wale columns
    list_display = [
        'title',
        'status',
        'category',
        'posted_by',
        'location',
        'date_lost_found',
        'is_verified',
        'is_resolved',
        'created_at',
    ]
    
    # Filter sidebar options
    list_filter = [
        'status',
        'category',
        'is_verified',
        'is_resolved',
        'created_at',
    ]
    
    # Search fields
    search_fields = [
        'title',
        'description',
        'location',
        'posted_by__username',
        'posted_by__email',
    ]
    
    # List view mein editable fields
    list_editable = [
        'is_verified',
        'is_resolved',
    ]
    
    # Ordering
    ordering = ['-created_at']
    
    # Detail view mein fields grouping
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'description', 'category', 'status']
        }),
        ('Image', {
            'fields': ['image'],
            'classes': ['collapse']  # Collapse by default
        }),
        ('Location & Date', {
            'fields': ['location', 'date_lost_found']
        }),
        ('Contact Information', {
            'fields': ['contact_email', 'contact_phone']
        }),
        ('User & Status', {
            'fields': ['posted_by', 'is_verified', 'is_resolved']
        }),
    ]
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Date hierarchy navigation
    date_hierarchy = 'created_at'
    
    # Items per page
    list_per_page = 25
    
    # Actions
    actions = ['mark_verified', 'mark_unverified', 'mark_resolved']
    
    def mark_verified(self, request, queryset):
        """
        Selected items ko verified mark karna.
        Admin bulk action ke liye.
        """
        count = queryset.update(is_verified=True)
        self.message_user(request, f'{count} items marked as verified.')
    mark_verified.short_description = 'Mark selected items as verified'
    
    def mark_unverified(self, request, queryset):
        """
        Selected items ko unverified mark karna.
        Admin bulk action ke liye.
        """
        count = queryset.update(is_verified=False)
        self.message_user(request, f'{count} items marked as unverified.')
    mark_unverified.short_description = 'Mark selected items as unverified'
    
    def mark_resolved(self, request, queryset):
        """
        Selected items ko resolved mark karna.
        Admin bulk action ke liye.
        """
        count = queryset.update(is_resolved=True)
        self.message_user(request, f'{count} items marked as resolved.')
    mark_resolved.short_description = 'Mark selected items as resolved'


# Admin site customization
admin.site.site_header = 'Campus Lost & Found Admin'
admin.site.site_title = 'Lost & Found Admin'
admin.site.index_title = 'Welcome to Campus Lost & Found Administration'
