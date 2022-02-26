from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect

from .models import User, Lead, Remark
from .forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.
@admin.action(description='Approve the selected users')
def approveUsersAction(modeladmin,request,queryset):
  queryset.update(is_approved = True)

class MyUserAdmin(UserAdmin):
  form = CustomUserChangeForm
  fieldsets = (
    (None,{
      'fields' : ('first_name','last_name','email','is_approved','user_type','manager_id')
    }),
    ('Permissions',{
      'fields' : ('is_staff','is_superuser','user_permissions')
    }),('Meta data',{
      'fields' : ('last_login','password')
    })
  )
  actions = [approveUsersAction]
  add_form = CustomUserCreationForm
  add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email','phone_number', 'password1', 'password2'),
        }),
    )
  ordering = ('first_name','last_name','date_joined',)
  readonly_fields = ('last_login','date_joined','user_actions')
  list_display = ('email','first_name', 'last_name','is_staff','is_superuser', 'is_approved','user_actions')
  search_fields = ('first_name', 'last_name', 'email')

  # CODE TO APPROVE USERS
  def get_urls(self):
      url = super().get_urls()
      myurl = [
        path('<id>/approve/',self.admin_site.admin_view(self.approve_user),name='approve_user'),
        path('<id>/notapprove/',self.admin_site.admin_view(self.not_approve_user),name='not_approve_user'),
      ]
      return myurl +url

  def user_actions(self,obj):
    if obj.is_approved:
      return format_html(
              '<a class="button" href="{}">not approve</a>&nbsp;',
              reverse('admin:not_approve_user',args=[obj.pk]),
          )
    else:
      return format_html(
              '<a class="button" href="{}">approve</a>&nbsp;',
              reverse('admin:approve_user',args=[obj.pk]),
          )
  
  user_actions.short_description = 'Approve user?'
  user_actions.allow_tags = True

  def approve_user(self,request,id,*args,**kwargs):
    try:
      user = User.objects.get(pk=id)
      user.is_approved = True
      user.save()
      self.message_user(request, f'Success, {user} is approved')
      return redirect('admin:authentication_user_changelist')
    except:
      self.message_user(request,'Some Error occured')
      return redirect('admin:authentication_user_changelist')



  def not_approve_user(self,request,id,*args,**kwargs):
    try:
      user = User.objects.get(pk=id)
      user.is_approved = False
      user.save()
      self.message_user(request, f'Success, {user} is not approved')
      return redirect('admin:authentication_user_changelist')
    except:
      self.message_user(request,'Some Error occured')
      return redirect('admin:authentication_user_changelist')
  
  def has_view_permission(self, request, obj= None) -> bool:
    user = request.user
    return user.is_superuser
  
  def has_change_permission(self, request, obj = None) -> bool:
    user = request.user
    return user.is_superuser

  def has_delete_permission(self, request, obj = None) -> bool:
    user = request.user
    return user.is_superuser
  
  def has_add_permission(self, request) -> bool:
    user = request.user
    return user.is_superuser

  # Only show Sales admin as a manager
  def render_change_form(self, request, context, *args, **kwargs):
    context['adminform'].form.fields['manager_id'].queryset = User.objects.filter(user_type=User.SALES_ADMIN)
    return super(MyUserAdmin, self).render_change_form(request, context, *args, **kwargs)
  
class MyLeadsAdmin(admin.ModelAdmin):

  def render_change_form(self, request, context, *args, **kwargs):
    context['adminform'].form.fields['user_id'].queryset = User.objects.filter(user_type=User.SALES_REPRESENTATIVE)
    return super(MyLeadsAdmin, self).render_change_form(request, context, *args, **kwargs)

class MyRemarksAdmin(admin.ModelAdmin):
  #PERMISSIONS
  def has_view_permission(self, request, obj= None) -> bool:
    user = request.user
    if user.is_superuser:
      return True
    if not obj or (obj and obj.user_id == user.id):
      return True
    return False
  
  def has_change_permission(self, request, obj = None) -> bool:
    user = request.user
    if user.is_superuser:
      return True
    if not obj or (obj and obj.user_id == user.id):
      return True
    return False

  def has_delete_permission(self, request, obj = None) -> bool:
    user = request.user
    if user.is_superuser:
      return True
    if not obj or (obj and obj.user_id == user.id):
      return True
    return False

  def render_change_form(self, request, context, *args, **kwargs):
    user = request.user
    context['adminform'].form.fields['user_id'].queryset = User.objects.filter(id = user.id)
    return super(MyRemarksAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(User,MyUserAdmin)
admin.site.register(Lead,MyLeadsAdmin)
admin.site.register(Remark,MyRemarksAdmin)
