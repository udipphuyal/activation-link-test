from django.shortcuts import render,redirect
from account.forms import RegistrationForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email
from account.models import User
from django.contrib.auth import authenticate ,login

# Create your views here.
def home(req):
    return render(req,'account/home.html')

def login_view(req):
    if req.user.is_authenticated:
        if req.user.is_seller:
            return redirect('seller_dashboard')
        elif req.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')
    if req.method=='POST':
        email=req.POST.get('email')
        password=req.POST.get('password')

        if not email and password:
           messages.error(req,'Both fields are required')
           return redirect('login')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(req,'Invalid email or password')
            return redirect('login')
        if not user.is_active:
            messages.error(req,'Your account is inactive.please activate your account')
            return redirect('login')
        
        user=authenticate(req,email=email,password=password)

        if user is not None:
            login(req, user)
            if user.is_seller:
                return redirect('seller_dashboard')
            elif user.is_customer:
                return redirect('customer_dashboard')
            else:
               messages.error(req,'you dont have permission to access this area')
               return redirect('home') 
        else:
            messages.error(req,'Invalid email or password')
            return redirect('login')
        
        
    
    return render(req,'account/login.html')

def register_view(req):
    if req.method=='POST':
        form=RegistrationForm(req.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active=False
            user.save()
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            activation_link=reverse('activate',kwargs={'uidb64':uidb64,'token':token})
            activation_url=f'{settings.SITE_DOMAIN} {activation_link}'
            send_activation_email(user.email,activation_url)
            messages.success(req,'Registration sucessfull ! please check your email to activate your account',)
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(req,'account/register.html',{'form':form})

def activate_account(req,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.object.get(pk=uid)

        if user.is_active:
            messages.warning(req,"This user has already been activated")
            return redirect('login')
        
        if default_token_generator.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(req,"Your account has been activated successfully")
            return redirect('login')
        else:
            messages.error(req,"The acctivation link is invalid or has expired")
            return redirect('login')
        
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        messages.error(req,"Invalid activation link")
        return redirect('lohin')

def password_reset_view(req):
    return render(req,'account/password_reset.html')


def password_reset_confirm_view(req,uidb64,token):
    return render(req,'account/password_reset_confirm.html')
