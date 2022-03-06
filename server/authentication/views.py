from distutils.log import error
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm, LoginForm
from .models import Lead, User, Remark
import json
# Create your views here.
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
  return JsonResponse({error : True})

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
  return render(request,'dashboard.html',context)

def homeView(request):
  return redirect('login')

def loginView(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():      
      user = authenticate(username=form.cleaned_data['email'],password=form.cleaned_data['password'])
      if user is None:
        messages.error(request,"Such user doesn't exist")
      else:
        login(request,user)
        messages.success(request,f"You are Successfully logged in as {user.get_full_name()}")
        return redirect('login')
    else:
      for error_field in form.errors:
        for error in form.errors[error_field]:
          messages.error(request,error)
  else:
    form = LoginForm()

  return render(request,'authentication/login.html',{
    'form' : form
  })

def registerView(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      print(form.cleaned_data)
      user = User(first_name = form.cleaned_data['first_name'],
                  last_name=form.cleaned_data['last_name'],
                  email = form.cleaned_data['email'],
                  phone_number = form.cleaned_data['phone_number'],
                )
      user.set_password(form.cleaned_data['password1'])
      user.save()
      messages.success(request,"You have sucessfully registered!")
      return redirect('login')
    else:
      for error_field in form.errors:
        for error in form.errors[error_field]:
          messages.error(request,error)
  else:
    form = CustomUserCreationForm()

  return render(request,'authentication/register.html',{
    'form' : form
  })

def logoutView(request):
  logout(request)
  return redirect('home')
  