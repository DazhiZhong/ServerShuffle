from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import requests

def requestview(request):
    context = {}
    if request.POST:
        url = request.POST.get('url',None)
        print(url, request.POST)
        if url[:4] != 'http':
            url = 'https://'+url
        try:
            stuff = requests.get(url, timeout=10)
        except:
            return redirect('request_view')
        return HttpResponse(content=stuff)
    return render(request, 'cards/req.html', context)


