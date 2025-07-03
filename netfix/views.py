from django.shortcuts import render, get_object_or_404
from django.db import models

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
    Shows customers who have requested their services
    """
    user = get_object_or_404(User, username=name)
    if hasattr(user, 'company'):
        company = user.company
        services = Service.objects.filter(company=company).order_by("-date_created")  # Company services display

        # Get service requests for this company's services
        service_requests = ServiceRequest.objects.filter(
            service__company=company
        ).select_related('customer__user', 'service').order_by('-request_date')

        # Calculate additional statistics for enhanced profile
        avg_price = services.aggregate(avg_price=models.Avg('price_hour'))['avg_price'] or 0
        unique_categories = services.values('field').distinct().count()
        total_requests = service_requests.count()

        # Calculate total revenue from requests
        total_revenue = sum(request.calculated_cost() for request in service_requests)

        # Calculate average request value
        avg_request_value = total_revenue / total_requests if total_requests > 0 else 0

        # Get unique customers who have requested services
        unique_customers = service_requests.values('customer').distinct().count()

        return render(request, 'users/company_profile.html', {
            'user': user,  # All company information
            'company': company,  # Company details
            'services': services,  # Available services
            'service_requests': service_requests,  # Service requests from customers
            'avg_price': avg_price,  # Average price per hour
            'unique_categories': unique_categories,  # Number of different service categories
            'total_requests': total_requests,  # Total service requests received
            'total_revenue': total_revenue,  # Total revenue from requests
            'avg_request_value': avg_request_value,  # Average value per request
            'unique_customers': unique_customers,  # Number of unique customers
        })
    else:
        return render(request, 'users/error.html', {'message': 'User is not a company'})
