from django.contrib import admin

from .models import Service, ServiceRequest


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_hour", "field", "date_created", "company")


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "service", "address", "hours_needed", "request_date")
