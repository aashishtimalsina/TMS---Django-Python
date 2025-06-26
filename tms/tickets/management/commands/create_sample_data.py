from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from services.models import Service, ServicePurchase
from tickets.models import ServiceTicket, LogTicket
from payments.models import Payment
from django.utils import timezone
from datetime import timedelta
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for the TMS application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@tms.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin',
                is_verified=True
            )
            self.stdout.write(f'Created admin user: {admin.username}')

        # Create some admin users
        admin_users = []
        for i in range(2):
            if not User.objects.filter(username=f'support{i+1}').exists():
                admin_user = User.objects.create_user(
                    username=f'support{i+1}',
                    email=f'support{i+1}@tms.com',
                    password='support123',
                    first_name='Support',
                    last_name=f'Agent {i+1}',
                    role='admin',
                    is_verified=True
                )
                admin_users.append(admin_user)
                self.stdout.write(f'Created admin user: {admin_user.username}')

        # Create client users
        client_users = []
        for i in range(5):
            if not User.objects.filter(username=f'client{i+1}').exists():
                client = User.objects.create_user(
                    username=f'client{i+1}',
                    email=f'client{i+1}@example.com',
                    password='client123',
                    first_name='Client',
                    last_name=f'User {i+1}',
                    role='client',
                    phone=f'555-000{i+1}',
                    company=f'Company {i+1}',
                    address=f'{i+1}23 Main St, City, State 1000{i+1}',
                    is_verified=True
                )
                client_users.append(client)
                self.stdout.write(f'Created client user: {client.username}')

        # Create services
        services_data = [
            {
                'name': 'Basic Support',
                'description': 'Basic technical support with email response within 24 hours.',
                'price': 29.99
            },
            {
                'name': 'Premium Support',
                'description': 'Premium support with priority handling and phone support.',
                'price': 59.99
            },
            {
                'name': 'Enterprise Support',
                'description': 'Enterprise-level support with dedicated account manager and 2-hour response time.',
                'price': 199.99
            },
            {
                'name': 'Cloud Hosting',
                'description': 'Reliable cloud hosting solution with 99.9% uptime guarantee.',
                'price': 89.99
            },
            {
                'name': 'Database Management',
                'description': 'Professional database management and optimization services.',
                'price': 149.99
            }
        ]

        services = []
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            services.append(service)
            if created:
                self.stdout.write(f'Created service: {service.name}')

        # Create service purchases for clients
        if client_users and services:
            for client in client_users:
                # Each client purchases 1-3 random services
                purchased_services = random.sample(services, random.randint(1, 3))
                for service in purchased_services:
                    if not ServicePurchase.objects.filter(user=client, service=service).exists():
                        purchase = ServicePurchase.objects.create(
                            user=client,
                            service=service,
                            status='active',
                            expiry_date=timezone.now() + timedelta(days=365)
                        )
                        
                        # Create corresponding payment
                        Payment.objects.create(
                            user=client,
                            service=service,
                            amount=service.price,
                            payment_method=random.choice(['credit_card', 'debit_card', 'paypal']),
                            status='completed',
                            completed_at=timezone.now() - timedelta(days=random.randint(1, 30))
                        )
                        
                        self.stdout.write(f'Created purchase: {client.username} -> {service.name}')

        # Create sample tickets
        ticket_titles = [
            'Login Issues',
            'Server Performance Problem',
            'Database Connection Error',
            'Email Configuration Help',
            'SSL Certificate Installation',
            'Backup Restoration Request',
            'Account Access Problem',
            'Feature Request - API Integration',
            'Security Vulnerability Report',
            'Migration Assistance Needed'
        ]

        ticket_descriptions = [
            'I am unable to log into my account. Getting authentication errors.',
            'The server response time has been very slow lately. Need investigation.',
            'Database connection keeps timing out. Please check the configuration.',
            'Need help setting up email forwarding and SMTP configuration.',
            'Require assistance with SSL certificate installation on the domain.',
            'Need to restore backup from last week due to data corruption.',
            'Cannot access my account dashboard. Getting permission denied errors.',
            'Would like to integrate our system with your API. Need documentation.',
            'Found a potential security issue in the user authentication system.',
            'Need help migrating our data from the old system to the new platform.'
        ]

        if client_users and services:
            for i in range(15):
                client = random.choice(client_users)
                # Get client's purchased services
                client_services = list(ServicePurchase.objects.filter(user=client, status='active').values_list('service', flat=True))
                
                if client_services:
                    service = Service.objects.get(pk=random.choice(client_services))
                else:
                    service = random.choice(services)

                ticket = ServiceTicket.objects.create(
                    title=random.choice(ticket_titles),
                    description=random.choice(ticket_descriptions),
                    client=client,
                    service=service,
                    status=random.choice(['open', 'pending', 'resolved']),
                    priority=random.choice(['low', 'medium', 'high', 'urgent']),
                    assigned_to=random.choice(admin_users) if admin_users and random.choice([True, False]) else None
                )
                
                # Create log entry for ticket creation
                LogTicket.objects.create(
                    ticket=ticket,
                    user=client,
                    action='created',
                    description=f'Ticket created by {client.username}'
                )
                
                # Randomly assign and add status changes
                if ticket.assigned_to:
                    LogTicket.objects.create(
                        ticket=ticket,
                        user=random.choice(admin_users) if admin_users else client,
                        action='assigned',
                        description=f'Ticket assigned to {ticket.assigned_to.username}'
                    )
                
                if ticket.status != 'open':
                    LogTicket.objects.create(
                        ticket=ticket,
                        user=ticket.assigned_to or random.choice(admin_users) if admin_users else client,
                        action='status_changed',
                        description=f'Status changed to {ticket.get_status_display()}'
                    )

                self.stdout.write(f'Created ticket: {ticket.ticket_id} - {ticket.title}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('')
        self.stdout.write('Login credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Support Agents: support1 / support123, support2 / support123')
        self.stdout.write('Clients: client1 / client123, client2 / client123, etc.')
