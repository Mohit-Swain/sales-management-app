from django.urls import path
from . import views

urlpatterns = [
  path('',views.homeView,name='home'),
  path('dashboard',views.dashboard,name='dashboard'),
  path('api/changeleadstate/<int:id>',views.changeLeadStatusAPI),
  path('api/getRemarks/<int:id>',views.getRemarks),
  path('api/addRemark/<int:id>',views.addRemark),
  path('api/getLeadCounts',views.getLeadCountsAPI),
  path('api/getTopSalesRep',views.getTopSalesRepAPI)
]
