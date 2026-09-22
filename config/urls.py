from django.urls import path
from django.views.generic import TemplateView
from ledgerly.views import *
from companies.views import dashboard

urlpatterns = [
    path("", TemplateView.as_view(template_name="Loginpage.html"), name="Loginpage"),
    path("Dashboard/", dashboard_protect, name="Dashboard"),
    path("register/", registration, name="register"),
    path("CheckUser/",CheckUser,name="CheckUser")
]