from django.urls import path
from . import views

urlpatterns = [
  path('',views.homeView,name='home'),
  path('login',views.loginView ,name='login'),
  path('logout',views.logoutView,name='logout'),
  path('register',views.registerView,name='register'),
  path('dashboard',views.dashboard,name='dashboard'),
  path('api/changeleadstate/<int:id>',views.changeLeadStatusAPI),
  path('api/getRemarks/<int:id>',views.getRemarks),
  path('api/addRemark/<int:id>',views.addRemark)
]
