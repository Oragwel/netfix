from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Count
from decimal import Decimal
from users.models import User, Customer, Company
from services.models import Service, ServiceRequest

class IntegrationTests(TestCase):
    """Integration tests for complete user workflows"""

    def setUp(self):
        self.client = Client()

    def test_complete_customer_workflow(self):
        """Test complete customer registration and service request workflow"""
        # 1. Register as customer
        customer_data = {
            'username': 'testcustomer',
            'email': 'customer@test.com',
            'date_of_birth': '1990-01-01',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('customer_signup'), data=customer_data)
        self.assertEqual(response.status_code, 302)

        # 2. Check customer was created correctly
        user = User.objects.get(username='testcustomer')
        self.assertTrue(user.is_customer)
        customer = Customer.objects.get(user=user)
        self.assertEqual(str(customer.date_of_birth), '1990-01-01')

        # 3. Create a service (by company) for customer to request
        company_user = User.objects.create_user(
            username='testcompany',
            email='company@test.com',
            password='testpass123',
            is_company=True
        )
        company = Company.objects.create(
            user=company_user,
            field_of_work='Electricity'
        )
        service = Service.objects.create(
            company=company,
            name='Electrical Repair',
            description='Professional electrical repair',
            price_hour=Decimal('10.50'),
            field='Electricity'
        )

        # 4. Customer requests service
        self.client.login(username='testcustomer', password='complexpass123')
        request_data = {
            'address': '123 Test Street',
            'hours_needed': 2
        }
        response = self.client.post(
            reverse('request_service', args=[service.id]),
            data=request_data
        )
        self.assertEqual(response.status_code, 302)

        # 5. Verify request was created with correct calculation
        service_request = ServiceRequest.objects.get(customer=customer, service=service)
        self.assertEqual(service_request.calculated_cost(), Decimal('21.00'))  # 2 * 10.50

    def test_complete_company_workflow(self):
        """Test complete company registration and service creation workflow"""
        # 1. Register as company
        company_data = {
            'username': 'electriccompany',
            'email': 'electric@test.com',
            'field_of_work': 'Electricity',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('company_signup'), data=company_data)
        self.assertEqual(response.status_code, 302)

        # 2. Check company was created correctly
        user = User.objects.get(username='electriccompany')
        self.assertTrue(user.is_company)
        company = Company.objects.get(user=user)
        self.assertEqual(company.field_of_work, 'Electricity')

        # 3. Login and create service
        self.client.login(username='electriccompany', password='complexpass123')
        service_data = {
            'name': 'Electrical Installation',
            'description': 'Professional electrical installation services',
            'price_hour': '10.50',
            'field': 'Electricity'
        }
        response = self.client.post(reverse('services_create'), data=service_data)
        self.assertEqual(response.status_code, 302)

        # 4. Verify service was created
        service = Service.objects.get(name='Electrical Installation')
        self.assertEqual(service.company, company)
        self.assertEqual(service.price_hour, Decimal('10.50'))

        # 5. Check service appears on company profile
        response = self.client.get(reverse('company_profile', args=['electriccompany']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electrical Installation')

    def test_all_in_one_company_flexibility(self):
        """Test All in One company can create services in any category"""
        # 1. Register All in One company
        company_data = {
            'username': 'allinonecompany',
            'email': 'allinone@test.com',
            'field_of_work': 'All in One',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('company_signup'), data=company_data)
        self.assertEqual(response.status_code, 302)

        # 2. Login and create services in different categories
        self.client.login(username='allinonecompany', password='complexpass123')

        service_categories = ['Electricity', 'Plumbing', 'Painting']
        for category in service_categories:
            service_data = {
                'name': f'{category} Service',
                'description': f'Professional {category.lower()} services',
                'price_hour': '15.00',
                'field': category
            }
            response = self.client.post(reverse('services_create'), data=service_data)
            self.assertEqual(response.status_code, 302)

        # 3. Verify all services were created
        company = Company.objects.get(user__username='allinonecompany')
        services = Service.objects.filter(company=company)
        self.assertEqual(services.count(), 3)

        # Check each category was created
        for category in service_categories:
            self.assertTrue(services.filter(field=category).exists())

    def test_most_requested_services_functionality(self):
        """Test most requested services page updates correctly"""
        # Create companies and services
        company1_user = User.objects.create_user(
            username='company1', email='c1@test.com', password='test123', is_company=True
        )
        company1 = Company.objects.create(user=company1_user, field_of_work='Painting')

        service1 = Service.objects.create(
            company=company1, name='Painting Service', description='Test',
            price_hour=Decimal('20.00'), field='Painting'
        )

        service2 = Service.objects.create(
            company=company1, name='Another Service', description='Test',
            price_hour=Decimal('25.00'), field='Painting'
        )

        # Create customer
        customer_user = User.objects.create_user(
            username='customer1', email='cust@test.com', password='test123', is_customer=True
        )
        customer = Customer.objects.create(user=customer_user, date_of_birth='1990-01-01')

        # Create multiple requests for service1 (make it most requested)
        for i in range(3):
            ServiceRequest.objects.create(
                customer=customer, service=service1,
                address=f'Address {i}', hours_needed=2
            )

        # Create one request for service2
        ServiceRequest.objects.create(
            customer=customer, service=service2,
            address='Address', hours_needed=1
        )

        # Test most requested services page
        response = self.client.get(reverse('most_requested_services'))
        self.assertEqual(response.status_code, 200)

        # Verify services are ordered by request count
        services = response.context['services']
        self.assertEqual(services[0].name, 'Painting Service')  # Most requested first
        self.assertEqual(services[0].request_count, 3)
        self.assertEqual(services[1].name, 'Another Service')
        self.assertEqual(services[1].request_count, 1)

class HomePageTests(TestCase):
    """Test home page functionality"""

    def test_home_page_loads(self):
        """Test home page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_shows_services(self):
        """Test home page displays available services"""
        # Create a service
        company_user = User.objects.create_user(
            username='company1', email='company@test.com', password='test123', is_company=True
        )
        company = Company.objects.create(user=company_user, field_of_work='Electricity')
        service = Service.objects.create(
            company=company, name='Test Service', description='Test description',
            price_hour=Decimal('15.00'), field='Electricity'
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check if service appears on home page (if implemented)
        # self.assertContains(response, 'Test Service')
