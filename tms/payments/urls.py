from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='payment_list'),
    path('<str:payment_id>/', views.PaymentDetailView.as_view(), name='payment_detail'),
    path('invoices/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('invoices/<str:invoice_number>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
]
