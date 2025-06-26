from django.urls import path
from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('tickets/', views.TicketListView.as_view(), name='ticket_list'),
    path('tickets/create/', views.TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/<str:ticket_id>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    path('tickets/<str:ticket_id>/edit/', views.TicketEditView.as_view(), name='ticket_edit'),
    path('tickets/<str:ticket_id>/comment/', views.TicketCommentCreateView.as_view(), name='ticket_comment'),
    path('tickets/<str:ticket_id>/close/', views.TicketCloseView.as_view(), name='ticket_close'),
    
    # Admin-only URLs
    path('admin/tickets/', views.AdminTicketListView.as_view(), name='admin_ticket_list'),
    path('admin/tickets/<str:ticket_id>/assign/', views.TicketAssignView.as_view(), name='ticket_assign'),
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
]
