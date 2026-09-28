from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from ledgerly.views import(
    CheckUser,
    registration,
    logout,
    dashboard_protect,
    company_panel,
    company_price,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="Loginpage.html"), name="Loginpage"),
    path("Dashboard/", dashboard_protect, name="Dashboard"),
    path("register/", registration, name="register"),
    path("CheckUser/",CheckUser,name="CheckUser"),
    path("logout/", logout, name="logout"),
    path("company/<int:company_id>/price/",company_price,name="company_price",),
    path("company/<int:company_id>/panel/",company_panel,name="company_panel",),
]

