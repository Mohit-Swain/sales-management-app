from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseForbidden
from .models import User
# Create your views here.

def home(request):
  return redirect('login')

def login(request):
  return render(request,'authentication/login.html')

def register(request):
  if request.method == 'GET':
    return render(request,'authentication/register.html')
  elif request.method == 'POST':
    pass
  else:
    return HttpResponseForbidden('This method is not allowed')