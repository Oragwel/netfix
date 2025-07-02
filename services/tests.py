from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from decimal import Decimal
from users.models import User, Customer, Company
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

class ServiceModelTests(TestCase):
    """Test Service model functionality"""

    def setUp(self):
        # Create company user
        self.company_user = User.objects.create_user(
            username='electriccompany',
            email='electric@test.com',
            password='testpass123',
            is_company=True
        )
        self.company = Company.objects.create(
            user=self.company_user,
            field_of_work='Electricity'
        )

    def test_service_creation(self):
        """Test basic service creation"""
        service = Service.objects.create(
            company=self.company,
            name='Electrical Repair',
            description='Professional electrical repair services',
            price_hour=Decimal('10.50'),
            field='Electricity'
        )
        self.assertEqual(service.name, 'Electrical Repair')
        self.assertEqual(service.price_hour, Decimal('10.50'))
        self.assertEqual(service.field, 'Electricity')
        self.assertEqual(service.company, self.company)

    def test_service_field_validation(self):
        """Test service field matches company specialization"""
        # Should work - matching field
        service = Service(
            company=self.company,
            name='Electrical Repair',
            description='Test service',
            price_hour=Decimal('10.50'),
            field='Electricity'
        )
        service.full_clean()  # Should not raise error

        # Should fail - non-matching field
        service_invalid = Service(
            company=self.company,
            name='Plumbing Service',
            description='Test service',
            price_hour=Decimal('10.50'),
            field='Plumbing'
        )
        with self.assertRaises(ValidationError):
            service_invalid.full_clean()

    def test_all_in_one_company_flexibility(self):
        """Test All in One companies can create any service type"""
        # Create All in One company
        all_in_one_user = User.objects.create_user(
            username='allinone',
            email='allinone@test.com',
            password='testpass123',
            is_company=True
        )
        all_in_one_company = Company.objects.create(
            user=all_in_one_user,
            field_of_work='All in One'
        )

        # Should be able to create any service type
        for field in ['Electricity', 'Plumbing', 'Painting']:
            service = Service(
                company=all_in_one_company,
                name=f'{field} Service',
                description='Test service',
                price_hour=Decimal('15.00'),
                field=field
            )
            service.full_clean()  # Should not raise error

    def test_cannot_create_all_in_one_service(self):
        """Test services cannot be categorized as 'All in One'"""
        service = Service(
            company=self.company,
            name='Test Service',
            description='Test service',
            price_hour=Decimal('10.50'),
            field='All in One'
        )
        with self.assertRaises(ValidationError):
            service.full_clean()

class ServiceRequestModelTests(TestCase):
    """Test ServiceRequest model functionality"""

    def setUp(self):
        # Create customer
        self.customer_user = User.objects.create_user(
            username='customer1',
            email='customer@test.com',
            password='testpass123',
            is_customer=True
        )
        self.customer = Customer.objects.create(
            user=self.customer_user,
            date_of_birth='1990-01-01'
        )

        # Create company and service
        self.company_user = User.objects.create_user(
            username='company1',
            email='company@test.com',
            password='testpass123',
            is_company=True
        )
        self.company = Company.objects.create(
            user=self.company_user,
            field_of_work='Electricity'
        )
        self.service = Service.objects.create(
            company=self.company,
            name='Electrical Repair',
            description='Professional electrical repair',
            price_hour=Decimal('10.50'),
            field='Electricity'
        )

    def test_service_request_creation(self):
        """Test service request creation"""
        request = ServiceRequest.objects.create(
            customer=self.customer,
            service=self.service,
            address='123 Test Street',
            hours_needed=2
        )
        self.assertEqual(request.customer, self.customer)
        self.assertEqual(request.service, self.service)
        self.assertEqual(request.address, '123 Test Street')
        self.assertEqual(request.hours_needed, 2)

    def test_calculated_cost(self):
        """Test automatic cost calculation (2 hours × 10.50 = 21.00)"""
        request = ServiceRequest.objects.create(
            customer=self.customer,
            service=self.service,
            address='123 Test Street',
            hours_needed=2
        )
        expected_cost = Decimal('21.00')  # 2 * 10.50
        self.assertEqual(request.calculated_cost(), expected_cost)

class ServiceFormTests(TestCase):
    """Test service creation form"""

    def setUp(self):
        self.company_user = User.objects.create_user(
            username='company1',
            email='company@test.com',
            password='testpass123',
            is_company=True
        )
        self.company = Company.objects.create(
            user=self.company_user,
            field_of_work='Electricity'
        )

    def test_valid_service_form(self):
        """Test valid service creation form"""
        form_data = {
            'name': 'Electrical Repair',
            'description': 'Professional electrical repair services',
            'price_hour': '10.50',
            'field': 'Electricity'
        }
        form = CreateNewService(data=form_data, company=self.company)
        self.assertTrue(form.is_valid())

    def test_field_restriction_for_specialized_company(self):
        """Test field choices are restricted for specialized companies"""
        form = CreateNewService(company=self.company)
        field_choices = form.fields['field'].choices
        # Should only have Electricity option
        self.assertEqual(len(field_choices), 1)
        self.assertEqual(field_choices[0], ('Electricity', 'Electricity'))

    def test_all_in_one_company_field_choices(self):
        """Test All in One companies get all field choices"""
        all_in_one_user = User.objects.create_user(
            username='allinone',
            email='allinone@test.com',
            password='testpass123',
            is_company=True
        )
        all_in_one_company = Company.objects.create(
            user=all_in_one_user,
            field_of_work='All in One'
        )

        form = CreateNewService(company=all_in_one_company)
        field_choices = form.fields['field'].choices
        # Should have all service field options (11 total)
        self.assertEqual(len(field_choices), 11)

class ServiceRequestFormTests(TestCase):
    """Test service request form"""

    def test_valid_request_form(self):
        """Test valid service request form"""
        form_data = {
            'address': '123 Test Street',
            'hours_needed': 2
        }
        form = RequestServiceForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_minimum_hours_validation(self):
        """Test minimum hours validation"""
        form_data = {
            'address': '123 Test Street',
            'hours_needed': 0  # Invalid - should be at least 1
        }
        form = RequestServiceForm(data=form_data)
        self.assertFalse(form.is_valid())

class ServiceViewTests(TestCase):
    """Test service-related views"""

    def setUp(self):
        self.client = Client()

        # Create company and service
        self.company_user = User.objects.create_user(
            username='company1',
            email='company@test.com',
            password='testpass123',
            is_company=True
        )
        self.company = Company.objects.create(
            user=self.company_user,
            field_of_work='Electricity'
        )
        self.service = Service.objects.create(
            company=self.company,
            name='Electrical Repair',
            description='Professional electrical repair',
            price_hour=Decimal('10.50'),
            field='Electricity'
        )

        # Create customer
        self.customer_user = User.objects.create_user(
            username='customer1',
            email='customer@test.com',
            password='testpass123',
            is_customer=True
        )
        self.customer = Customer.objects.create(
            user=self.customer_user,
            date_of_birth='1990-01-01'
        )

    def test_service_list_view(self):
        """Test all services page"""
        response = self.client.get(reverse('services_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electrical Repair')

    def test_individual_service_view(self):
        """Test individual service page displays all required information"""
        response = self.client.get(reverse('index', args=[self.service.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electrical Repair')
        self.assertContains(response, '10.50')
        self.assertContains(response, 'Electricity')
        self.assertContains(response, 'company1')

    def test_service_field_view(self):
        """Test service type pages"""
        response = self.client.get(reverse('services_field', args=['electricity']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Electrical Repair')

    def test_service_creation_requires_company_login(self):
        """Test service creation requires company authentication"""
        response = self.client.get(reverse('services_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_service_creation_by_company(self):
        """Test service creation by logged-in company"""
        self.client.login(username='company1', password='testpass123')

        form_data = {
            'name': 'New Service',
            'description': 'New electrical service',
            'price_hour': '15.00',
            'field': 'Electricity'
        }
        response = self.client.post(reverse('services_create'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation

        # Check service was created
        self.assertTrue(Service.objects.filter(name='New Service').exists())

    def test_service_request_by_customer(self):
        """Test service request by customer"""
        self.client.login(username='customer1', password='testpass123')

        form_data = {
            'address': '123 Test Street',
            'hours_needed': 2
        }
        response = self.client.post(
            reverse('request_service', args=[self.service.id]),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)  # Redirect after request

        # Check request was created
        request = ServiceRequest.objects.get(customer=self.customer, service=self.service)
        self.assertEqual(request.address, '123 Test Street')
        self.assertEqual(request.hours_needed, 2)
        self.assertEqual(request.calculated_cost(), Decimal('21.00'))

    def test_most_requested_services_view(self):
        """Test most requested services page"""
        response = self.client.get(reverse('most_requested_services'))
        self.assertEqual(response.status_code, 200)
