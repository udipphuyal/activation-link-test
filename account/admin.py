from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User 
# Register your models here.
class UserModelAdmin(UserAdmin):
    model=User
    list_display=["id","email","name","is_active","is_seller","is_customer","is_staff","is_superuser"]
    list_filter=["is_superuser"]
    fieldsets=[("User Credentials",{"fields":["email","password"]}),
               ("Personal Information",{"fields":["name"]}),
               ("Permissions",{"fields":["is_active","is_staff","is_superuser","is_customer","is_seller"]})
               ]
    add_fieldsets=[
        (None,
         {
             "classes":["wide"],
             "fields":["email","password1","password2"],
         },
        ),
    ]
    search_fields=["email"]
    ordering=["email","id"]
    filter_horizontal=[]

admin.site.register(User, UserModelAdmin)