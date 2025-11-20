from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# Create your models here.

class Usermanager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)
     
    def create_user(self,email,password=None):
        if not email:
            raise ValueError("User must have a valid email")
        user=self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extrafields):
        extrafields.setdefault('is_staff',True)
        extrafields.setdefault('is_superuser',True)
        if extrafields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff True")
        

        if extrafields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_staff True")
        user=self.create_user(email,password)
        user.is_staff=True
        user.is_superuser=True
        user.is_seller=True
        user.is_customer=True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=True)
    is_seller=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD='email'
    objects=Usermanager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        "Does the user has a special permission" 
        return self.is_superuser
    
    def has_module_perms(self,applabel):
        "Does the user have a permission to view the app label"
        return self.is_superuser