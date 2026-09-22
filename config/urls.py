from django.urls import path
from django.views.generic import TemplateView
from ledgerly.views import *

urlpatterns = [
    path("", TemplateView.as_view(template_name="Loginpage.html"), name="Loginpage"),
    path("Dashboard/", TemplateView.as_view(template_name="Dashboard.html"), name="dashboard"),
    path("register/", registration, name="register"),
    path("CheckUser/",CheckUser,name="CheckUser")
]