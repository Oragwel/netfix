from django.shortcuts import render, get_object_or_404

from users.models import User, Company, Customer
from services.models import Service, ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    """
    Customer Profile Display - Shows all customer information (except password)
    Shows service requests with correct price calculation (2 hours × 10.50 = 21.00)
    """
    user = get_object_or_404(User, username=name)
    if hasattr(user, 'customer'):
        customer = user.customer
        service_requests = ServiceRequest.objects.filter(customer=customer).order_by('-request_date')  # Service requests display

        # Calculate statistics for customer profile
        total_spent = sum(request.calculated_cost() for request in service_requests)  # Price calculation
        unique_companies = service_requests.values('service__company').distinct().count()
        unique_categories = service_requests.values('service__field').distinct().count()

        return render(request, 'users/customer_profile.html', {
            'user': user,
            'customer': customer,
            'service_requests': service_requests,
            'total_spent': total_spent,
            'unique_companies': unique_companies,
            'unique_categories': unique_categories,
        })
    else:
        return render(request, 'users/error.html', {'message': 'User is not a customer'})


def company_profile(request, name):
    """
    Company Profile Display - Shows all company information (except password)
    Shows services created by company as available services
    """
    user = get_object_or_404(User, username=name)
    if hasattr(user, 'company'):
        company = user.company
        services = Service.objects.filter(company=company).order_by("-date_created")  # Company services display
        return render(request, 'users/profile.html', {
            'user': user,  # All company information
            'company': company,  # Company details
            'services': services  # Available services
        })
    else:
        return render(request, 'users/error.html', {'message': 'User is not a company'})
