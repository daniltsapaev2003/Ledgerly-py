from django.shortcuts import render, redirect
from .models import User
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password 
from django.contrib.auth.hashers import check_password


def registration(request):
    if request.method == "POST":
        try:
                User.objects.create(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                email=request.POST["email"],
                phone_number=request.POST["phone_number"],
                password=make_password(request.POST["password"])
                )
                request.session["session"] =  User.objects.filter(email = request.POST["email"]).first().id
                return redirect("Dashboard")

        except IntegrityError:
            return render(
                request,
                "Loginpage.html",
                {"user_exists": True}
            )

    return 0

def CheckUser(request):
    user_data = User.objects.filter(email = request.POST["email"])
    password = request.POST["password"]
    if user_data.exists():
         if check_password(password,user_data.first().password):
              request.session["session"] = user_data.first().id
              return redirect("Dashboard")
    return render(
                    request,
                    "Loginpage.html",
                    {"wrong_email_password": True}
                )   


def dashboard_protect(request):
    if "session" in request.session:
        return render(request, "Dashboard.html")
    return redirect("Loginpage")
     