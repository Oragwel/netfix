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
        super().__init__(*args, **kwargs)
        self.fields['price_hour'].validators = [MinValueValidator(0.01)]


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
