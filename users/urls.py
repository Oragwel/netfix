from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("customer/", views.CustomerSignUpView.as_view(), name="customer_signup"),
    path("company/", views.CompanySignUpView.as_view(), name="company_signup"),
    path("login/", views.LoginUserView, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_redirect, name="profile_redirect"),
]
