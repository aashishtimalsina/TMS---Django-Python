from django.contrib import admin
from .models import Payment, Invoice

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'service', 'amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'user__username', 'user__email', 'service__name', 'transaction_id')
    ordering = ('-created_at',)
    readonly_fields = ('payment_id', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('payment_id', 'user', 'service', 'amount', 'payment_method')
        }),
        ('Status & Transaction', {
            'fields': ('status', 'transaction_id', 'gateway_response', 'completed_at')
        }),
        ('Additional Info', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'user', 'total_amount', 'status', 'due_date', 'issued_date')
    list_filter = ('status', 'issued_date', 'due_date')
    search_fields = ('invoice_number', 'user__username', 'user__email')
    ordering = ('-issued_date',)
    readonly_fields = ('invoice_number', 'issued_date')
    
    fieldsets = (
        (None, {
            'fields': ('invoice_number', 'user', 'payment')
        }),
        ('Amount Details', {
            'fields': ('amount', 'tax_amount', 'total_amount')
        }),
        ('Status & Dates', {
            'fields': ('status', 'due_date', 'issued_date', 'paid_date')
        }),
        ('Additional Info', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
