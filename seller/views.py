from django.shortcuts import render

# Create your views here.
def seller_dashboard_view(req):
    return render(req,'seller/dashboard.html')