from django.contrib import admin
from .models import Service, ServicePurchase

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'is_active')
        }),
    )

@admin.register(ServicePurchase)
class ServicePurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'status', 'purchase_date', 'expiry_date')
    list_filter = ('status', 'purchase_date', 'service')
    search_fields = ('user__username', 'user__email', 'service__name')
    ordering = ('-purchase_date',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'service', 'status', 'expiry_date', 'notes')
        }),
    )
