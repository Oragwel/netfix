from django.core.validators import MinValueValidator
from django.db import models
from users.models import Company, Customer

class Service(models.Model):
    FIELD_CHOICES = [
        ("Air Conditioner", "Air Conditioner"),
        ("Carpentry", "Carpentry"),
        ("Electricity", "Electricity"),
        ("Gardening", "Gardening"),
        ("Home Machines", "Home Machines"),
        ("Housekeeping", "Housekeeping"),  # ✅ Fixed spelling from "House Keeping"
        ("Interior Design", "Interior Design"),
        ("Locks", "Locks"),
        ("Painting", "Painting"),
        ("Plumbing", "Plumbing"),
        ("Water Heaters", "Water Heaters"),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=8, validators=[MinValueValidator(0.00)])  # ✅ Fixed max_digits from 100 to 8 for realistic pricing
    field = models.CharField(max_length=30, choices=FIELD_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)  # ✅ Changed from auto_now=True to auto_now_add=True

class ServiceRequest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    hours_needed = models.PositiveIntegerField()
    request_date = models.DateTimeField(auto_now_add=True)

    def calculated_cost(self):
        return self.service.price_hour * self.hours_needed
