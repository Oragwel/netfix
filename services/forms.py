from django import forms
from django.core.validators import MinValueValidator

from users.models import Company
from .models import Service, ServiceRequest


class CreateNewService(forms.ModelForm):
    """ Form for companies to create new services """

    class Meta:
        model = Service
        fields = ['name', 'description', 'price_hour', 'field']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter Service Name',
                'autocomplete': 'off',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter Description',
                'class': 'form-control',
                'rows': 4
            }),
            'price_hour': forms.NumberInput(attrs={
                'placeholder': 'Enter Price per Hour',
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),
            'field': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        # Extract company from kwargs if provided
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        self.fields['price_hour'].validators = [MinValueValidator(0.01)]

        # Restrict field choices based on company's field of work
        if self.company:
            if self.company.field_of_work == "All in One":
                # "All in One" companies can create services in any specific field
                # (All service fields are available since "All in One" is already removed from FIELD_CHOICES)
                available_choices = Service.FIELD_CHOICES
            else:
                # Other companies can only create services in their specific field
                available_choices = [(self.company.field_of_work, self.company.field_of_work)]

            self.fields['field'].choices = available_choices

            # Add help text to explain the restriction
            if self.company.field_of_work != "All in One":
                self.fields['field'].help_text = f"Your company specializes in {self.company.field_of_work} services."
            else:
                self.fields['field'].help_text = "As an 'All in One' company, you can create services in any category."

    def clean(self):
        """Additional validation for service field restrictions"""
        cleaned_data = super().clean()
        field = cleaned_data.get('field')

        # Prevent "All in One" services (this should not happen due to form choices, but extra safety)
        if field == "All in One":
            raise forms.ValidationError(
                "Services cannot be categorized as 'All in One'. "
                "Please choose a specific service category."
            )

        if self.company and field:
            # "All in One" companies can create services in any specific field
            if self.company.field_of_work == "All in One":
                # No additional restrictions for All in One companies
                pass
            else:
                # Specialized companies can only create services in their specific field
                if self.company.field_of_work != field:
                    raise forms.ValidationError(
                        f"Your company specializes in '{self.company.field_of_work}' services. "
                        f"You cannot create services in the '{field}' category."
                    )

        return cleaned_data

    def save(self, commit=True):
        """Override save to set company before saving"""
        instance = super().save(commit=False)
        if self.company:
            instance.company = self.company
        if commit:
            instance.save()
        return instance


class RequestServiceForm(forms.ModelForm):
    """ Form for customers to request a service """

    class Meta:
        model = ServiceRequest
        fields = ['address', 'hours_needed']
        widgets = {
            'address': forms.TextInput(attrs={
                'placeholder': 'Enter your address',
                'class': 'form-control'
            }),
            'hours_needed': forms.NumberInput(attrs={
                'placeholder': 'Number of hours needed',
                'class': 'form-control',
                'min': 1
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hours_needed'].validators = [MinValueValidator(1)]
