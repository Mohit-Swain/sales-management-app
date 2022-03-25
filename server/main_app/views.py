import imp
from django.shortcuts import render, redirect
from django.http import JsonResponse
from authentication.models import Remark, Lead, User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.timezone import utc
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta
import json

# Create your views here.
def homeView(request):
  if request.user.is_authenticated:
    if request.user.is_superuser:
      return redirect('analytics')
    return redirect('dashboard')
  return redirect('login')

def analyticsView(request):
  return render(request,'main_app/analytics.html')

@login_required(login_url=reverse_lazy('login'))
def addRemark(request,id):
  if request.method == 'POST':
    try:
      body = json.loads(request.body)
      new_remark = body.get('remark')
      if not new_remark:
        return JsonResponse({'error' : True, 'message' : "empty remark can't be added"})
      Remark.objects.create(remark=new_remark,lead_id=Lead.objects.get(id=id),user_id=request.user)
      return JsonResponse({'success': True})
    except Exception as e:
      return JsonResponse({'error' : True, 'message' : str(e)})
  return JsonResponse({'error' : True})


@login_required(login_url=reverse_lazy('login'))
def getRemarks(request,id):
  if request.method == 'GET':
    remarks = Remark.objects.filter(lead_id = id)
    remarks = list(remarks.values('remark','lead_id','user_id','created_at','user_id__first_name','user_id__last_name','user_id__email'))
    return JsonResponse({'remarks' : remarks})
  return JsonResponse({'error' : True})


@login_required(login_url=reverse_lazy('login'))
def changeLeadStatusAPI(request,id):
  if request.method == 'POST':
    try:
      body = json.loads(request.body)
      lead = Lead.objects.get(id=id)
      value = body.get('value')
      lead.state = value
      lead.save()
      return JsonResponse({'success': True})
    except Exception as e:
      return JsonResponse({'error' : True, 'message' : str(e)})
  return JsonResponse({'error' : True})


@login_required(login_url=reverse_lazy('login'))
def dashboard(request):
  leads = Lead.objects.filter(user_id=request.user.id).order_by('-created_at')
  filter = request.GET.get('filter')
  if filter:
    if filter == 'NEW':
      leads = leads.filter(state__isnull = True)
    else:
      leads = leads.filter(state=filter)
  p = Paginator(leads,10)
  page_number = request.GET.get('page')
  p_leads = p.get_page(page_number)
  status_text = {
    Lead.HOT : 'Hot Lead',
    Lead.COLD : 'Cold Lead',
    Lead.MEDIUM : 'Med Lead',
    Lead.GREY : 'Grey',
    Lead.SUCCESS: 'Success'
  }
  status_bootstrap_color = {
    Lead.HOT : 'danger',
    Lead.COLD : 'info',
    Lead.MEDIUM : 'warning',
    Lead.GREY : 'secondary',
    Lead.SUCCESS: 'success',
  }
  context = {
    'leads' : p_leads,
    'status_text' : status_text,
    'status_bootstrap_color' : status_bootstrap_color
  }
  return render(request,'main_app/dashboard.html',context)

def getLeadCountsAPI(request):
  now = datetime.utcnow().replace(tzinfo=utc)
  last_three_month = now - timedelta(days=90)
  last_three_month_leads = Lead.objects.filter(created_at__gte=last_three_month)
  TOTAL_COUNT = last_three_month_leads.count()
  HOT_COUNT = last_three_month_leads.filter(state=Lead.HOT).count()
  MEDIUM_COUNT = last_three_month_leads.filter(state=Lead.MEDIUM).count()
  GREY_COUNT = last_three_month_leads.filter(state=Lead.GREY).count()
  return JsonResponse({
    'total_leads' : TOTAL_COUNT,
    'hot_leads' : HOT_COUNT,
    'med_leads' : MEDIUM_COUNT,
    'grey_leads' : GREY_COUNT
  })

def getTopSalesRepAPI(request):
  now = datetime.utcnow().replace(tzinfo=utc)
  last_month = now - timedelta(days=30)
  top_users = User.objects \
        .annotate(success_count=Count('lead',filter= Q(lead__state=Lead.SUCCESS) & Q(lead__updated_at__gte=last_month)))\
        .order_by('-success_count') \
        .values('id','first_name','last_name','email','success_count')[:10]

  return JsonResponse({'success': True,'sales_representatives': list(top_users)})

def getDailyLeadStatistics(request):
  today = datetime.today().replace(tzinfo=utc)
  enddate = TruncDay(today + timedelta(days=1))
  startdate = TruncDay(today - timedelta(days=6))
  
  query = Lead.objects \
            .annotate(day=TruncDay('updated_at')) \
            .filter(day__range=[startdate,enddate]) \
            .values('state','day') \
            .annotate(count_state=Count('state')) \
            .order_by('day')

  query = list(query)
  result = {}
  for item in query:
    hash = item['day'].strftime('%d/%m')
    if not hash in result:
      result[hash] = {}
    result[hash][item['state']] = item['count_state']

  modified_result = {
    'days': [],
    'hot' : [],
    'med' : [],
    'grey' : []
  }
  for item in result:
    modified_result['days'].append(item)
    modified_result['hot'].append(result[item].get(Lead.HOT,0))
    modified_result['med'].append(result[item].get(Lead.MEDIUM,0))
    modified_result['grey'].append(result[item].get(Lead.GREY,0))



  
  return JsonResponse(modified_result,safe=False)