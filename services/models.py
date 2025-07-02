from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from users.models import Company, Customer

class Service(models.Model):
    """
    Service Creation & Display - Asks for name, description, price, field
    Displays name, description, field, price per hour, date created, company name
    """
    FIELD_CHOICES = [
        # Service categories matching company field restrictions
        # Note: "All in One" excluded - services must have specific categories
        ("Air Conditioner", "Air Conditioner"),
        ("Carpentry", "Carpentry"),
        ("Electricity", "Electricity"),
        ("Gardening", "Gardening"),
        ("Home Machines", "Home Machines"),
        ("Housekeeping", "Housekeeping"),
        ("Interior Design", "Interior Design"),
        ("Locks", "Locks"),
        ("Painting", "Painting"),
        ("Plumbing", "Plumbing"),
        ("Water Heaters", "Water Heaters"),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Company association
    name = models.CharField(max_length=40)  # Service name
    description = models.TextField()  # Service description
    price_hour = models.DecimalField(decimal_places=2, max_digits=8, validators=[MinValueValidator(0.00)])  # Price field
    field = models.CharField(max_length=30, choices=FIELD_CHOICES)  # Service field/category
    date_created = models.DateTimeField(auto_now_add=True)  # Date created for display

    def clean(self):
        """
        All in One Company Service Creation Rules:
        - All in One companies can choose between all service types
        - Specialized companies restricted to their field of work
        - Services cannot be categorized as 'All in One' (must be specific)
        """
        super().clean()

        # Prevent "All in One" services - services must have specific categories
        if self.field == "All in One":
            raise ValidationError(
                "Services cannot be categorized as 'All in One'. "
                "Please choose a specific service category (e.g., Plumbing, Electricity, etc.)."
            )

        # Validate company field restrictions for service creation
        if hasattr(self, 'company') and self.company and self.field:
            # "All in One" companies can create services in any specific field
            if self.company.field_of_work == "All in One":
                return  # No restrictions for All in One companies

            # Specialized companies can only create services in their specific field
            if self.company.field_of_work != self.field:
                raise ValidationError(
                    f"Your company specializes in '{self.company.field_of_work}' services. "
                    f"You cannot create services in the '{self.field}' category. "
                    f"Please choose '{self.company.field_of_work}' or register as an 'All in One' company."
                )

    def save(self, *args, **kwargs):
        """Override save to call clean validation"""
        self.clean()
        super().save(*args, **kwargs)

class ServiceRequest(models.Model):
    """
    Service Request System - Asks for address, service time (hours)
    Calculates total cost (hours × price_per_hour)
    Appears on customer profile with correct price calculation
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Customer association
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Service association
    address = models.CharField(max_length=255)  # Address field
    hours_needed = models.PositiveIntegerField()  # Service time in hours
    request_date = models.DateTimeField(auto_now_add=True)  # Request tracking

    def calculated_cost(self):
        """Price Calculation - Shows correct calculation: 2 hours × 10.50 = 21.00"""
        return self.service.price_hour * self.hours_needed  # Automatic cost calculation
