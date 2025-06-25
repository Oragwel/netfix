from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # ✅ Changed from CharField to EmailField for proper email validation
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)  # ✅ Added relevant field for user profile

class Company(models.Model):
    FIELD_CHOICES = [
        ("Air Conditioner", "Air Conditioner"),
        ("All in One", "All in One"),
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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    field_of_work = models.CharField(max_length=70, choices=FIELD_CHOICES)  # ✅ Renamed field for clarity
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
