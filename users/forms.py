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
        raise ValidationError(f"{value} is already taken.")


class CustomerSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=DateInput)  # ✅ Added proper field for capturing customer birthdate
    email = forms.EmailField(validators=[validate_email])  # ✅ Integrated email validation function

    class Meta:
        model = User
        fields = ["username", "email", "date_of_birth", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True  # ✅ Ensured correct role assignment for customers
        if commit:
            user.save()
            Customer.objects.create(user=user)  # ✅ Auto-create related Customer instance
        return user


class CompanySignUpForm(UserCreationForm):
    field_of_work = forms.ChoiceField(choices=Company.FIELD_CHOICES)  # ✅ Dynamically loads choices for company specialization
    email = forms.EmailField(validators=[validate_email])  # ✅ Ensured unique email validation

    class Meta:
        model = User
        fields = ["username", "email", "field_of_work", "password1", "password2"]

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
