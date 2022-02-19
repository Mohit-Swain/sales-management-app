from django.shortcuts import redirect, render
from django.http import HttpResponse
# Create your views here.

def home(request):
  return redirect('login')

def login(request):
  return render(request,'authentication/login.html')

def register(request):
  return render(request,'authentication/register.html')