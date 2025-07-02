from users.models import Company
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

def index(request, id):
    """
    Individual Service Page - Displays name, description, field, price per hour, date created, company name
    """
    service = get_object_or_404(Service, id=id)  # Individual service page access

    # Get other services from the same company (excluding current service)
    other_services = Service.objects.filter(
        company=service.company
    ).exclude(id=service.id).order_by('-date_created')[:3]

    # Get related services in the same category (excluding current service)
    related_services = Service.objects.filter(
        field=service.field
    ).exclude(id=service.id).order_by('-date_created')[:3]

    context = {
        'service': service,  # Service with all required info
        'other_services': other_services,
        'related_services': related_services,
    }

    return render(request, "services/single_service.html", context)

def create(request):
    # Check if user is authenticated and is a company
    if not request.user.is_authenticated:
        return redirect('/register/login/')

    if not request.user.is_company:
        return render(request, 'users/error.html', {'message': 'Only companies can create services.'})

    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        return render(request, 'users/error.html', {'message': 'Company profile not found.'})

    if request.method == "POST":
        form = CreateNewService(request.POST, company=company)
        if form.is_valid():
            service = form.save(commit=False)
            service.company = company
            service.save()
            return redirect("services_list")
    else:
        form = CreateNewService(company=company)

    return render(request, "services/create.html", {"form": form, "company": company})

# Added missing function to get the service list
def service_list(request):
    """All Services Page - Shows every service created by every company"""
    services = Service.objects.all().order_by("-date_created")  # All services page
    return render(request, "services/list.html", {"services": services})


def most_requested_services(request):
    """Most Requested Services Page - Shows most requested services and updates when new requests are made"""
    services = Service.objects.annotate(
        request_count=Count('servicerequest')
    ).order_by('-request_count', '-date_created')  # Most requested ordering

    return render(request, "services/most_requested.html", {
        "services": services,  # Updated list with request counts
        "page_title": "Most Requested Services"
    })


def service_field(request, field):
    """Service Type Pages - Has page for every type of service displaying services of that type"""
    field = field.replace("-", " ").title()  # Convert slug format back to readable text
    services = Service.objects.filter(field=field)  # Services by specific type
    return render(request, "services/field.html", {"services": services, "field": field})


def request_service(request, id):
    service = get_object_or_404(Service, id=id)  # ✅ Used get_object_or_404() for better error handling

    # Check if user is authenticated and is a customer
    if not request.user.is_authenticated:
        return redirect('/register/login/')

    if not request.user.is_customer:
        return render(request, 'users/error.html', {'message': 'Only customers can request services.'})

    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.customer = request.user.customer  # ✅ Ensured only customers can request services
            request_instance.service = service
            request_instance.save()
            # Redirect to customer profile with the username parameter
            return redirect(f'/customer/{request.user.username}')
    else:
        form = RequestServiceForm()

    return render(request, "services/request_service.html", {"form": form, "service": service})
