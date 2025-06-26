from django.contrib import admin
from .models import ServiceTicket, LogTicket, TicketComment, TicketAttachment

class LogTicketInline(admin.TabularInline):
    model = LogTicket
    extra = 0
    readonly_fields = ('created_at',)
    
class TicketCommentInline(admin.TabularInline):
    model = TicketComment
    extra = 0
    readonly_fields = ('created_at',)

class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 0
    readonly_fields = ('uploaded_at',)

@admin.register(ServiceTicket)
class ServiceTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'title', 'client', 'service', 'priority', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'priority', 'service', 'created_at', 'assigned_to')
    search_fields = ('ticket_id', 'title', 'client__username', 'client__email')
    ordering = ('-created_at',)
    readonly_fields = ('ticket_id', 'created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('ticket_id', 'title', 'description', 'client', 'service')
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status', 'priority', 'resolved_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [TicketCommentInline, TicketAttachmentInline, LogTicketInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif hasattr(request.user, 'role') and request.user.role == 'admin':
            return qs
        else:
            return qs.filter(client=request.user)

@admin.register(LogTicket)
class LogTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'action', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('ticket__ticket_id', 'user__username', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('ticket__ticket_id', 'user__username', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'original_name', 'uploaded_by', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('ticket__ticket_id', 'original_name', 'uploaded_by__username')
    ordering = ('-uploaded_at',)
    readonly_fields = ('uploaded_at',)
