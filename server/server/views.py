from django.shortcuts import render

def handle404(request,exception):
  return render(request,'404.html')