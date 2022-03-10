from django.shortcuts import render, redirect
from django.http import JsonResponse
from authentication.models import Remark, Lead
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import json

# Create your views here.
def homeView(request):
  if request.user.is_authenticated:
    return redirect('dashboard')
  return redirect('login')

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