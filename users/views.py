from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate 
from django.views.generic import CreateView, TemplateView  

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer


def register(request):
    """  Renders the registration page where users choose to sign up as a customer or company """
    return render(request, 'users/register.html')


class CustomerSignUpView(CreateView):
    """ Handles customer signup using Django's built-in CreateView """
    model = User  
    form_class = CustomerSignUpForm 
    template_name = 'users/register_customer.html'

    def get_context_data(self, **kwargs):
        """ Adds extra context to indicate this is a customer registration process """
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """ Saves the new customer and logs them in automatically """
        user = form.save()
        login(self.request, user) 
        return redirect('/')


class CompanySignUpView(CreateView):
    """ Handles company signup using CreateView """
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    def get_context_data(self, **kwargs):
        """ Adds extra context to indicate this is a company registration process """
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """ Saves the new company and logs them in automatically """
        user = form.save()
        login(self.request, user)
        return redirect('/')


def LoginUserView(request):
    """ Placeholder function - Needs implementation for handling user authentication """
    pass
