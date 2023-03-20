from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
# Create your views here.

def index(request):
    responseData = render_to_string("login\login.html")
    return HttpResponse(responseData)