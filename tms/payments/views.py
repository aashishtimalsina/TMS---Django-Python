from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Payment, Invoice


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_admin():
            queryset = Payment.objects.select_related('user', 'service').order_by('-created_at')
        else:
            queryset = Payment.objects.filter(user=self.request.user).select_related('service').order_by('-created_at')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(payment_id__icontains=search) |
                Q(service__name__icontains=search) |
                Q(transaction_id__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['status_choices'] = Payment.STATUS_CHOICES
        return context


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'
    slug_field = 'payment_id'
    slug_url_kwarg = 'payment_id'
    
    def get_queryset(self):
        if self.request.user.is_admin():
            return Payment.objects.select_related('user', 'service')
        return Payment.objects.filter(user=self.request.user).select_related('service')


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'payments/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10
    
    def get_queryset(self):
        if self.request.user.is_admin():
            queryset = Invoice.objects.select_related('user', 'payment').order_by('-issued_date')
        else:
            queryset = Invoice.objects.filter(user=self.request.user).select_related('payment').order_by('-issued_date')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(invoice_number__icontains=search) |
                Q(user__username__icontains=search) if self.request.user.is_admin() else Q(invoice_number__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', '')
        context['status_choices'] = Invoice.STATUS_CHOICES
        return context


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'payments/invoice_detail.html'
    context_object_name = 'invoice'
    slug_field = 'invoice_number'
    slug_url_kwarg = 'invoice_number'
    
    def get_queryset(self):
        if self.request.user.is_admin():
            return Invoice.objects.select_related('user', 'payment')
        return Invoice.objects.filter(user=self.request.user).select_related('payment')
