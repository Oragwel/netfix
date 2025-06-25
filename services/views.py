from users.models import Company
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Service, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

def index(request, id):
    service = get_object_or_404(Service, id=id)  # ✅ Used get_object_or_404() instead of Service.objects.get() to prevent crashes
    return render(request, "services/single_service.html", {"service": service})

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
    services = Service.objects.all().order_by("-date_created")
    return render(request, "services/list.html", {"services": services})


def most_requested_services(request):
    """Display services ordered by number of requests (most requested first)"""
    services = Service.objects.annotate(
        request_count=Count('servicerequest')
    ).order_by('-request_count', '-date_created')

    return render(request, "services/most_requested.html", {
        "services": services,
        "page_title": "Most Requested Services"
    })


# Added missing function to get the service field
def service_field(request, field):
    field = field.replace("-", " ").title()  # ✅ Convert slug format back to readable text
    services = Service.objects.filter(field=field)  # ✅ Retrieve services by category
    return render(request, "services/field.html", {"services": services, "field": field})


def request_service(request, id):
    service = get_object_or_404(Service, id=id)  # ✅ Used get_object_or_404() for better error handling
    if request.method == "POST":
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.customer = request.user.customer  # ✅ Ensured only customers can request services
            request_instance.service = service
            request_instance.save()
            return redirect("customer_profile")  # ✅ Redirects after successful request submission
    else:
        form = RequestServiceForm()

    return render(request, "services/request_service.html", {"form": form, "service": service})
