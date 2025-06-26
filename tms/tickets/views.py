from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q, Count
from django.utils import timezone
from django import forms
from .models import ServiceTicket, LogTicket, TicketComment
from accounts.models import User


class TicketForm(forms.ModelForm):
    class Meta:
        model = ServiceTicket
        fields = ['title', 'description', 'service', 'priority']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})


class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment', 'is_internal']
        
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        if not user.is_admin():
            # Hide internal field for clients
            del self.fields['is_internal']


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tickets/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.is_admin():
            # Admin dashboard
            context.update({
                'total_tickets': ServiceTicket.objects.count(),
                'open_tickets': ServiceTicket.objects.filter(status='open').count(),
                'pending_tickets': ServiceTicket.objects.filter(status='pending').count(),
                'resolved_tickets': ServiceTicket.objects.filter(status='resolved').count(),
                'recent_tickets': ServiceTicket.objects.order_by('-created_at')[:5],
                'total_users': User.objects.filter(role='client').count(),
            })
        else:
            # Client dashboard
            context.update({
                'total_tickets': user.tickets.count(),
                'open_tickets': user.tickets.filter(status='open').count(),
                'pending_tickets': user.tickets.filter(status='pending').count(),
                'resolved_tickets': user.tickets.filter(status='resolved').count(),
                'recent_tickets': user.tickets.order_by('-created_at')[:5],
            })
        
        return context


class TicketListView(LoginRequiredMixin, ListView):
    model = ServiceTicket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = ServiceTicket.objects.filter(client=self.request.user).order_by('-created_at')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(ticket_id__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['priority'] = self.request.GET.get('priority', '')
        context['status_choices'] = ServiceTicket.STATUS_CHOICES
        context['priority_choices'] = ServiceTicket.PRIORITY_CHOICES
        return context


class AdminTicketListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = ServiceTicket
    template_name = 'tickets/admin_ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.is_admin()
    
    def get_queryset(self):
        queryset = ServiceTicket.objects.select_related('client', 'assigned_to', 'service').order_by('-created_at')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(ticket_id__icontains=search) |
                Q(client__username__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
            
        # Filter by assigned user
        assigned = self.request.GET.get('assigned')
        if assigned:
            queryset = queryset.filter(assigned_to_id=assigned)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['priority'] = self.request.GET.get('priority', '')
        context['assigned'] = self.request.GET.get('assigned', '')
        context['status_choices'] = ServiceTicket.STATUS_CHOICES
        context['priority_choices'] = ServiceTicket.PRIORITY_CHOICES
        context['admin_users'] = User.objects.filter(role='admin')
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = ServiceTicket
    form_class = TicketForm
    template_name = 'tickets/ticket_create.html'
    
    def form_valid(self, form):
        form.instance.client = self.request.user
        response = super().form_valid(form)
        
        # Create log entry
        LogTicket.objects.create(
            ticket=self.object,
            user=self.request.user,
            action='created',
            description=f'Ticket created by {self.request.user.username}'
        )
        
        messages.success(self.request, f'Ticket {self.object.ticket_id} created successfully!')
        return response
    
    def get_success_url(self):
        return reverse('tickets:ticket_detail', kwargs={'ticket_id': self.object.ticket_id})


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = ServiceTicket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'
    slug_field = 'ticket_id'
    slug_url_kwarg = 'ticket_id'
    
    def get_queryset(self):
        if self.request.user.is_admin():
            return ServiceTicket.objects.all()
        return ServiceTicket.objects.filter(client=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('created_at')
        context['logs'] = self.object.logs.order_by('-created_at')
        context['comment_form'] = TicketCommentForm(self.request.user)
        
        # Add admin users for assignment dropdown
        if self.request.user.is_admin():
            context['admin_users'] = User.objects.filter(role='admin')
            
        return context


class TicketEditView(LoginRequiredMixin, UpdateView):
    model = ServiceTicket
    form_class = TicketForm
    template_name = 'tickets/ticket_edit.html'
    slug_field = 'ticket_id'
    slug_url_kwarg = 'ticket_id'
    
    def get_queryset(self):
        if self.request.user.is_admin():
            return ServiceTicket.objects.all()
        return ServiceTicket.objects.filter(client=self.request.user, status__in=['open', 'pending'])
    
    def form_valid(self, form):
        # Track changes for logging
        old_values = {}
        new_values = {}
        
        for field in ['title', 'description', 'priority', 'status']:
            if hasattr(form.instance, field):
                old_val = getattr(self.get_object(), field, None)
                new_val = getattr(form.instance, field, None)
                if old_val != new_val:
                    old_values[field] = old_val
                    new_values[field] = new_val
        
        response = super().form_valid(form)
        
        # Create log entries for changes
        if old_values:
            LogTicket.objects.create(
                ticket=self.object,
                user=self.request.user,
                action='updated',
                description=f'Ticket updated by {self.request.user.username}',
                old_value=str(old_values),
                new_value=str(new_values)
            )
        
        messages.success(self.request, 'Ticket updated successfully!')
        return response
    
    def get_success_url(self):
        return reverse('tickets:ticket_detail', kwargs={'ticket_id': self.object.ticket_id})


class TicketCommentCreateView(LoginRequiredMixin, CreateView):
    model = TicketComment
    form_class = TicketCommentForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        ticket = get_object_or_404(ServiceTicket, ticket_id=self.kwargs['ticket_id'])
        
        # Check permissions
        if not self.request.user.is_admin() and ticket.client != self.request.user:
            messages.error(self.request, 'You do not have permission to comment on this ticket.')
            return redirect('tickets:ticket_detail', ticket_id=ticket.ticket_id)
        
        form.instance.ticket = ticket
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Create log entry
        LogTicket.objects.create(
            ticket=ticket,
            user=self.request.user,
            action='comment_added',
            description=f'Comment added by {self.request.user.username}'
        )
        
        messages.success(self.request, 'Comment added successfully!')
        return response
    
    def get_success_url(self):
        return reverse('tickets:ticket_detail', kwargs={'ticket_id': self.kwargs['ticket_id']})


class TicketAssignView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ServiceTicket
    fields = ['assigned_to', 'status']
    slug_field = 'ticket_id'
    slug_url_kwarg = 'ticket_id'
    
    def test_func(self):
        return self.request.user.is_admin()
    
    def form_valid(self, form):
        old_assigned = self.get_object().assigned_to
        old_status = self.get_object().status
        
        response = super().form_valid(form)
        
        # Create log entries
        if old_assigned != form.instance.assigned_to:
            LogTicket.objects.create(
                ticket=self.object,
                user=self.request.user,
                action='assigned',
                description=f'Ticket assigned to {form.instance.assigned_to}',
                old_value=str(old_assigned),
                new_value=str(form.instance.assigned_to)
            )
        
        if old_status != form.instance.status:
            LogTicket.objects.create(
                ticket=self.object,
                user=self.request.user,
                action='status_changed',
                description=f'Status changed from {old_status} to {form.instance.status}',
                old_value=old_status,
                new_value=form.instance.status
            )
        
        messages.success(self.request, 'Ticket updated successfully!')
        return response
    
    def get_success_url(self):
        return reverse('tickets:ticket_detail', kwargs={'ticket_id': self.object.ticket_id})


class TicketCloseView(LoginRequiredMixin, UpdateView):
    model = ServiceTicket
    fields = []
    slug_field = 'ticket_id'
    slug_url_kwarg = 'ticket_id'
    
    def get_queryset(self):
        if self.request.user.is_admin():
            return ServiceTicket.objects.all()
        return ServiceTicket.objects.filter(client=self.request.user)
    
    def form_valid(self, form):
        form.instance.status = 'resolved'
        form.instance.resolved_at = timezone.now()
        response = super().form_valid(form)
        
        # Create log entry
        LogTicket.objects.create(
            ticket=self.object,
            user=self.request.user,
            action='resolved',
            description=f'Ticket resolved by {self.request.user.username}'
        )
        
        messages.success(self.request, 'Ticket closed successfully!')
        return response
    
    def get_success_url(self):
        return reverse('tickets:ticket_detail', kwargs={'ticket_id': self.object.ticket_id})


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'tickets/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def test_func(self):
        return self.request.user.is_admin()
    
    def get_queryset(self):
        queryset = User.objects.filter(role='client').annotate(
            ticket_count=Count('tickets')
        ).order_by('-date_joined')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | 
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context
