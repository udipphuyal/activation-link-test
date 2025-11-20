from django.shortcuts import render

# Create your views here.
def customer_dashboard_view(req):
    return render(req,'customer/dashboard.html')


def password_change_view(req):
    return render(req,'customer/password_change.html')