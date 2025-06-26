from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ServiceTicket, LogTicket
from services.models import Service

User = get_user_model()


class ServiceTicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='client'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.service = Service.objects.create(
            name='Test Service',
            description='Test service description',
            price=99.99
        )
        
    def test_create_ticket(self):
        ticket = ServiceTicket.objects.create(
            title='Test Ticket',
            description='This is a test ticket',
            client=self.user,
            service=self.service
        )
        
        self.assertEqual(ticket.title, 'Test Ticket')
        self.assertEqual(ticket.client, self.user)
        self.assertEqual(ticket.service, self.service)
        self.assertEqual(ticket.status, 'open')
        self.assertEqual(ticket.priority, 'medium')
        self.assertIsNotNone(ticket.ticket_id)
        self.assertTrue(ticket.ticket_id.startswith('TKT-'))
        
    def test_ticket_string_representation(self):
        ticket = ServiceTicket.objects.create(
            title='Test Ticket',
            description='This is a test ticket',
            client=self.user
        )
        self.assertEqual(str(ticket), f'{ticket.ticket_id} - Test Ticket')
        
    def test_automatic_ticket_id_generation(self):
        ticket1 = ServiceTicket.objects.create(
            title='Ticket 1',
            description='First ticket',
            client=self.user
        )
        ticket2 = ServiceTicket.objects.create(
            title='Ticket 2',
            description='Second ticket',
            client=self.user
        )
        
        self.assertNotEqual(ticket1.ticket_id, ticket2.ticket_id)
        self.assertTrue(ticket1.ticket_id.startswith('TKT-'))
        self.assertTrue(ticket2.ticket_id.startswith('TKT-'))


class LogTicketModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='client'
        )
        self.ticket = ServiceTicket.objects.create(
            title='Test Ticket',
            description='This is a test ticket',
            client=self.user
        )
        
    def test_create_log_ticket(self):
        log = LogTicket.objects.create(
            ticket=self.ticket,
            user=self.user,
            action='created',
            description='Ticket was created'
        )
        
        self.assertEqual(log.ticket, self.ticket)
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, 'created')
        self.assertEqual(log.description, 'Ticket was created')
        
    def test_log_ticket_string_representation(self):
        log = LogTicket.objects.create(
            ticket=self.ticket,
            user=self.user,
            action='created',
            description='Ticket was created'
        )
        self.assertEqual(str(log), f'{self.ticket.ticket_id} - Created')


class TicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='client'
        )
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            role='admin'
        )
        self.service = Service.objects.create(
            name='Test Service',
            description='Test service description',
            price=99.99
        )
        
    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('tickets:dashboard'))
        self.assertEqual(response.status_code, 302)
        
    def test_dashboard_authenticated_client(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        
    def test_dashboard_authenticated_admin(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('tickets:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        
    def test_ticket_list_requires_login(self):
        response = self.client.get(reverse('tickets:ticket_list'))
        self.assertEqual(response.status_code, 302)
        
    def test_ticket_list_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Tickets')
        
    def test_ticket_create_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:ticket_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create New Support Ticket')
        
    def test_ticket_create_post(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('tickets:ticket_create'), {
            'title': 'Test Ticket',
            'description': 'This is a test ticket',
            'service': self.service.pk,
            'priority': 'high'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ServiceTicket.objects.filter(title='Test Ticket').exists())
        
    def test_admin_ticket_list_requires_admin(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tickets:admin_ticket_list'))
        self.assertEqual(response.status_code, 403)
        
    def test_admin_ticket_list_admin_access(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('tickets:admin_ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'All Support Tickets')
