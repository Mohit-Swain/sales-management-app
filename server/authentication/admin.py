from email.headerregistry import Group
from django.contrib import admin
from .models import User, Lead, Remark
# Register your models here.

admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Remark)
