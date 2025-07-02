from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User, Customer, Company
from .forms import CustomerSignUpForm, CompanySignUpForm

class UserModelTests(TestCase):
    """Test User model functionality"""

    def test_user_creation(self):
        """Test basic user creation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_customer)
        self.assertFalse(user.is_company)

    def test_email_uniqueness(self):
        """Test email uniqueness constraint"""
        User.objects.create_user(
            username='user1',
            email='test@example.com',
            password='testpass123'
        )

        # Try to create another user with same email
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='user2',
                email='test@example.com',
                password='testpass123'
            )

class CustomerModelTests(TestCase):
    """Test Customer model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='customer1',
            email='customer@example.com',
            password='testpass123',
            is_customer=True
        )

    def test_customer_creation(self):
        """Test customer profile creation"""
        customer = Customer.objects.create(
            user=self.user,
            date_of_birth='1990-01-01'
        )
        self.assertEqual(customer.user, self.user)
        self.assertEqual(str(customer.date_of_birth), '1990-01-01')

class CompanyModelTests(TestCase):
    """Test Company model functionality"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='company1',
            email='company@example.com',
            password='testpass123',
            is_company=True
        )

    def test_company_creation(self):
        """Test company profile creation"""
        company = Company.objects.create(
            user=self.user,
            field_of_work='Electricity'
        )
        self.assertEqual(company.user, self.user)
        self.assertEqual(company.field_of_work, 'Electricity')
        self.assertEqual(company.rating, 0)  # Default rating

    def test_field_choices_validation(self):
        """Test field of work choices are restricted"""
        valid_fields = [
            'Air Conditioner', 'All in One', 'Carpentry', 'Electricity',
            'Gardening', 'Home Machines', 'Housekeeping', 'Interior Design',
            'Locks', 'Painting', 'Plumbing', 'Water Heaters'
        ]

        for field in valid_fields:
            company = Company(user=self.user, field_of_work=field)
            # Should not raise validation error
            company.full_clean()

class CustomerSignUpFormTests(TestCase):
    """Test Customer registration form"""

    def test_valid_customer_form(self):
        """Test valid customer registration"""
        form_data = {
            'username': 'newcustomer',
            'email': 'customer@test.com',
            'date_of_birth': '1990-01-01',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomerSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_username_uniqueness_validation(self):
        """Test username uniqueness validation"""
        # Create existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@test.com',
            password='testpass123'
        )

        form_data = {
            'username': 'existinguser',  # Same username
            'email': 'new@test.com',
            'date_of_birth': '1990-01-01',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomerSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_email_uniqueness_validation(self):
        """Test email uniqueness validation"""
        # Create existing user
        User.objects.create_user(
            username='existing',
            email='existing@test.com',
            password='testpass123'
        )

        form_data = {
            'username': 'newuser',
            'email': 'existing@test.com',  # Same email
            'date_of_birth': '1990-01-01',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomerSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_customer_creation_on_save(self):
        """Test that Customer profile is created when form is saved"""
        form_data = {
            'username': 'newcustomer',
            'email': 'customer@test.com',
            'date_of_birth': '1990-01-01',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomerSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertTrue(user.is_customer)
        self.assertFalse(user.is_company)

        # Check Customer profile was created
        customer = Customer.objects.get(user=user)
        self.assertEqual(str(customer.date_of_birth), '1990-01-01')

class CompanySignUpFormTests(TestCase):
    """Test Company registration form"""

    def test_valid_company_form(self):
        """Test valid company registration"""
        form_data = {
            'username': 'newcompany',
            'email': 'company@test.com',
            'field_of_work': 'Electricity',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CompanySignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_company_creation_on_save(self):
        """Test that Company profile is created when form is saved"""
        form_data = {
            'username': 'newcompany',
            'email': 'company@test.com',
            'field_of_work': 'Electricity',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CompanySignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertTrue(user.is_company)
        self.assertFalse(user.is_customer)

        # Check Company profile was created
        company = Company.objects.get(user=user)
        self.assertEqual(company.field_of_work, 'Electricity')

class UserViewTests(TestCase):
    """Test user registration and authentication views"""

    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        """Test registration page loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'customer')
        self.assertContains(response, 'company')

    def test_customer_registration_view(self):
        """Test customer registration view"""
        response = self.client.get(reverse('customer_signup'))
        self.assertEqual(response.status_code, 200)

        # Test POST request
        form_data = {
            'username': 'testcustomer',
            'email': 'customer@test.com',
            'date_of_birth': '1990-01-01',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('customer_signup'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

        # Check user was created
        user = User.objects.get(username='testcustomer')
        self.assertTrue(user.is_customer)
        self.assertTrue(Customer.objects.filter(user=user).exists())

    def test_company_registration_view(self):
        """Test company registration view"""
        response = self.client.get(reverse('company_signup'))
        self.assertEqual(response.status_code, 200)

        # Test POST request
        form_data = {
            'username': 'testcompany',
            'email': 'company@test.com',
            'field_of_work': 'Electricity',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = self.client.post(reverse('company_signup'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

        # Check user was created
        user = User.objects.get(username='testcompany')
        self.assertTrue(user.is_company)
        self.assertTrue(Company.objects.filter(user=user).exists())

    def test_profile_pages(self):
        """Test profile pages display correctly"""
        # Create customer
        customer_user = User.objects.create_user(
            username='customer1',
            email='customer@test.com',
            password='testpass123',
            is_customer=True
        )
        Customer.objects.create(user=customer_user, date_of_birth='1990-01-01')

        # Create company
        company_user = User.objects.create_user(
            username='company1',
            email='company@test.com',
            password='testpass123',
            is_company=True
        )
        Company.objects.create(user=company_user, field_of_work='Electricity')

        # Test customer profile
        response = self.client.get(reverse('customer_profile', args=['customer1']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'customer1')

        # Test company profile
        response = self.client.get(reverse('company_profile', args=['company1']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'company1')
