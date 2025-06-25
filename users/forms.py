from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from users.models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = "date"  # ✅ Modified input type for consistency with date fields


# ✅ Optimized email validation to use Django's standard validation methods
def validate_email(value):
    """Ensures email uniqueness across User model"""
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"The email '{value}' is already registered. Please use a different email.")

def validate_username(value):
    """Ensures username uniqueness across User model"""
    if User.objects.filter(username=value).exists():
        raise ValidationError(f"The username '{value}' is already taken. Please choose a different username.")

# Removed CustomerRegistrationForm as it's not used and has incorrect fields
        
class CustomerSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=DateInput)  # ✅ Added proper field for capturing customer birthdate
    email = forms.EmailField()  # ✅ Email field for customer registration

    class Meta:
        model = User
        fields = ["username", "email", "date_of_birth", "password1", "password2"]

    def clean_username(self):
        """Validate username uniqueness"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"The username '{username}' is already taken. Please choose a different username.")
        return username

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"The email '{email}' is already registered. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True  # ✅ Ensured correct role assignment for customers
        if commit:
            user.save()
            Customer.objects.create(user=user, date_of_birth=self.cleaned_data.get('date_of_birth'))  # ✅ Auto-create related Customer instance with date_of_birth
        return user


class CompanySignUpForm(UserCreationForm):
    field_of_work = forms.ChoiceField(choices=Company.FIELD_CHOICES)  # ✅ Dynamically loads choices for company specialization
    email = forms.EmailField()  # ✅ Email field for company registration

    class Meta:
        model = User
        fields = ["username", "email", "field_of_work", "password1", "password2"]

    def clean_username(self):
        """Validate username uniqueness"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(f"The username '{username}' is already taken. Please choose a different username.")
        return username

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"The email '{email}' is already registered. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True  # ✅ Correctly assigns company role upon signup
        if commit:
            user.save()
            Company.objects.create(user=user, field_of_work=self.cleaned_data["field_of_work"])  # ✅ Auto-create related Company instance with correct field
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Enter Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"}))

    def clean_email(self):
        """Ensures the user exists before attempting login"""  # ✅ Added validation logic to improve authentication handling
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No account found with this email.")
        return email
