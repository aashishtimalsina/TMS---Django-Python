# Django Ticket Management System (TMS)

A comprehensive ticket management system built with Django and AdminLTE for beautiful UI. This system provides role-based authentication, service management, ticket tracking, and payment processing.

## Features

### 🎯 Core Features
- **Role-based Authentication**: Admin and Client roles with different permissions
- **Service Management**: Clients can browse and purchase services
- **Ticket System**: Create, track, and manage support tickets
- **Payment Processing**: Handle payments and generate invoices
- **Activity Logging**: Track all ticket activities and changes
- **Search & Filter**: Advanced search and filtering capabilities
- **Responsive UI**: AdminLTE-based beautiful and responsive interface

### 🔐 User Roles

#### Admin Users
- Manage all tickets across the system
- Assign tickets to support agents
- View all users and their activities
- Access Django admin panel
- View payment and invoice data
- Update ticket statuses and priorities

#### Client Users
- Register and manage their profile
- Purchase services
- Create support tickets
- Track ticket progress
- View payment history
- Add comments to tickets

### 🎨 UI Features
- **AdminLTE 3.2**: Modern and responsive dashboard
- **Bootstrap 4**: Mobile-first responsive design
- **Font Awesome**: Beautiful icons throughout the interface
- **DataTables**: Advanced table features with pagination
- **Charts**: Dashboard statistics and analytics
- **Notifications**: Real-time feedback system

## Installation

### Prerequisites
- Python 3.8+
- Django 5.2+
- SQLite (default) or PostgreSQL/MySQL for production

### Setup Instructions

1. **Clone the repository**
```bash
git clone <repository-url>
cd ticket_management_system/tms
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create sample data (optional)**
```bash
python manage.py create_sample_data
```

6. **Start the development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Main application: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/

## Default Login Credentials

### Admin Users
- **Username**: admin | **Password**: admin123
- **Username**: support1 | **Password**: support123
- **Username**: support2 | **Password**: support123

### Client Users
- **Username**: client1 | **Password**: client123
- **Username**: client2 | **Password**: client123
- **Username**: client3 | **Password**: client123
- **Username**: client4 | **Password**: client123
- **Username**: client5 | **Password**: client123

## Project Structure

```
tms/
├── accounts/                   # User authentication and profile management
│   ├── models.py              # Custom User model
│   ├── views.py               # Authentication views
│   ├── admin.py               # Admin configuration
│   └── templates/accounts/    # Authentication templates
├── tickets/                   # Ticket management system
│   ├── models.py              # Ticket, Log, Comment models
│   ├── views.py               # Ticket CRUD operations
│   ├── admin.py               # Ticket admin interface
│   └── templates/tickets/     # Ticket templates
├── services/                  # Service management
│   ├── models.py              # Service and Purchase models
│   ├── views.py               # Service views
│   └── templates/services/    # Service templates
├── payments/                  # Payment processing
│   ├── models.py              # Payment and Invoice models
│   ├── views.py               # Payment views
│   └── templates/payments/    # Payment templates
├── templates/                 # Global templates
│   ├── base.html              # Main layout with AdminLTE
│   └── auth_base.html         # Authentication layout
├── static/                    # Static files (CSS, JS, Images)
├── media/                     # Uploaded files
└── tms/                       # Project configuration
    ├── settings.py            # Django settings
    └── urls.py                # URL configuration
```

## Models Overview

### User Model (Custom)
- Extended Django's AbstractUser
- Role-based permissions (admin/client)
- Additional fields: phone, address, company, verification status

### Service Models
- **Service**: Available services with pricing
- **ServicePurchase**: Track user service purchases

### Ticket Models
- **ServiceTicket**: Main ticket entity with status workflow
- **LogTicket**: Activity logging for audit trails
- **TicketComment**: Comments and communication
- **TicketAttachment**: File attachments support

### Payment Models
- **Payment**: Payment transactions with status tracking
- **Invoice**: Generated invoices for payments

## Key Features Implemented

### 🎫 Ticket Management
- **Ticket Creation**: Clients can create tickets for purchased services
- **Status Workflow**: Open → Pending → Resolved
- **Priority Levels**: Low, Medium, High, Urgent
- **Assignment System**: Admins can assign tickets to agents
- **Activity Logging**: All changes are tracked and logged
- **Comments System**: Internal and external communication

### 💳 Payment System
- **Service Purchases**: Clients can purchase services
- **Payment Tracking**: Complete payment lifecycle management
- **Invoice Generation**: Automatic invoice creation
- **Payment History**: Detailed payment records

### 🔍 Search & Filter
- **Global Search**: Search across tickets, users, payments
- **Advanced Filters**: Filter by status, priority, date ranges
- **Pagination**: Efficient data display with pagination
- **Sorting**: Multiple column sorting capabilities

### 📊 Dashboard & Analytics
- **Statistics Cards**: Quick overview of key metrics
- **Recent Activity**: Latest tickets and updates
- **Role-based Data**: Different views for admins and clients
- **Charts & Graphs**: Visual data representation

## Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **User Authentication**: Secure login/logout system
- **Permission Checks**: Role-based access control
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping enabled

## Testing

Run the test suite:
```bash
python manage.py test
```

Tests cover:
- Model functionality and relationships
- View permissions and responses
- Form validation
- Authentication workflows
- CRUD operations

## Production Deployment

### Environment Variables
Create a `.env` file for production:
```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

### Static Files
```bash
python manage.py collectstatic
```

### Database Migration
```bash
python manage.py migrate --settings=tms.settings.production
```

## API Endpoints

The system provides web-based interface with the following main URL patterns:

- `/` - Dashboard (redirects to login if not authenticated)
- `/accounts/` - Authentication (login, register, profile)
- `/dashboard/` - Main dashboard and ticket management
- `/services/` - Service browsing and purchasing
- `/payments/` - Payment history and invoices
- `/admin/` - Django admin interface

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Technologies Used

- **Backend**: Django 5.2, Python 3.8+
- **Frontend**: AdminLTE 3.2, Bootstrap 4, jQuery
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **Forms**: Django Crispy Forms with Bootstrap 4
- **Icons**: Font Awesome 6
- **Charts**: Chart.js (can be added for analytics)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Ticket Management System** - Built with ❤️ using Django and AdminLTE
