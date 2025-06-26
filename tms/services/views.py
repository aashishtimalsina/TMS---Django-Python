from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Service, ServicePurchase
from payments.models import Payment


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = 'services/service_list.html'
    context_object_name = 'services'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True).order_by('name')
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = 'services/service_detail.html'
    context_object_name = 'service'
    
    def get_queryset(self):
        return Service.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if user already purchased this service
        context['already_purchased'] = ServicePurchase.objects.filter(
            user=self.request.user,
            service=self.object,
            status='active'
        ).exists()
        return context


class ServicePurchaseView(LoginRequiredMixin, CreateView):
    model = ServicePurchase
    fields = []
    
    def get(self, request, *args, **kwargs):
        service = get_object_or_404(Service, pk=kwargs['pk'], is_active=True)
        
        # Check if already purchased
        existing_purchase = ServicePurchase.objects.filter(
            user=request.user,
            service=service,
            status='active'
        ).first()
        
        if existing_purchase:
            messages.warning(request, 'You have already purchased this service.')
            return redirect('services:service_detail', pk=service.pk)
        
        # Create service purchase
        purchase = ServicePurchase.objects.create(
            user=request.user,
            service=service,
            status='active',
            expiry_date=timezone.now() + timedelta(days=365)  # 1 year
        )
        
        # Create payment record
        payment = Payment.objects.create(
            user=request.user,
            service=service,
            amount=service.price,
            payment_method='credit_card',  # Default for demo
            status='completed',  # Auto-complete for demo
            completed_at=timezone.now()
        )
        
        messages.success(request, f'Successfully purchased {service.name}! You can now create tickets for this service.')
        return redirect('services:my_services')


class MyServicesView(LoginRequiredMixin, ListView):
    model = ServicePurchase
    template_name = 'services/my_services.html'
    context_object_name = 'purchases'
    paginate_by = 10
    
    def get_queryset(self):
        return ServicePurchase.objects.filter(user=self.request.user).select_related('service').order_by('-purchase_date')
