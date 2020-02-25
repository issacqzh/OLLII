from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
	return render(request,'html_sites/home.html')

def about(request):
	return render(request,'html_sites/about.html')

def help4mom(request):
	return render(request,'html_sites/help4mom.html')

def vocabulary(request):
	return render(request,'html_sites/vocabulary.html')

def later(request):
	return render(request,'html_sites/later.html')