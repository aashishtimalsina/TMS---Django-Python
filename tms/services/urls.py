from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='service_list'),
    path('<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('<int:pk>/purchase/', views.ServicePurchaseView.as_view(), name='service_purchase'),
    path('my-services/', views.MyServicesView.as_view(), name='my_services'),
]
