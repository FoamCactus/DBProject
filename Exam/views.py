from django.shortcuts import render
from django.http import HttpResponse
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def studentSignIn(request):
    if request.method == "POST":
        get_value= request.body
    data = {}
    return HttpResponse(json.dumps(data), content_type="application/json")