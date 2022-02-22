from email.headerregistry import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Lead, Remark
from .forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.

class MyUserAdmin(UserAdmin):
  form = CustomUserChangeForm
  fieldsets = (
    (None,{
      'fields' : ('first_name','last_name','email','is_approved','user_type','manager_id')
    }),
    ('Permissions',{
      'fields' : ('is_staff','is_superuser')
    }),('Meta data',{
      'fields' : ('last_login','password')
    })
  )
  add_form = CustomUserCreationForm
  add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email','phone_number', 'password1', 'password2'),
        }),
    )
  ordering = ('first_name','last_name','date_joined',)
  readonly_fields = ('last_login',)
  list_display = ('email', 'first_name', 'last_name', 'user_type')
  search_fields = ('first_name', 'last_name', 'email')

admin.site.register(User,MyUserAdmin)
admin.site.register(Lead)
admin.site.register(Remark)
