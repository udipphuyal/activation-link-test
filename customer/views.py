from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def customer_dashboard_view(req):
    return render(req,'customer/dashboard.html')

@login_required
def password_change_view(req):
    if req.method=='POST':
        form=PasswordChangeForm(user=req.user,data=req.POST)
        if form.is_valid():
            form.save()
            logout(req)
            messages.success(req,'password changed successfully. please login with your new password')
            return redirect('login')
        
        else:
            for fields,errors in form.errors.items():
                for error in errors:
                    messages.error(req,error)
    else:
        form =PasswordChangeForm(user=req.user)
    return render(req,'customer/password_change.html')