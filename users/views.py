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
    """ Handles user authentication using email and password """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Get user by email since we're using email for login
            try:
                user = User.objects.get(email=email)
                # Authenticate using username (Django's default) but with email lookup
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error('password', 'Invalid password.')
            except User.DoesNotExist:
                form.add_error('email', 'No account found with this email.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})
