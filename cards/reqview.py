from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import requests
from bs4 import BeautifulSoup as soup

def requestview(request):
    context = {}
    print(request.GET)
    if request.POST or request.GET.get('url',None) is not None:
        if request.POST:
            url = request.POST.get('url',None)
        else:
            url = request.GET.get('url',None)
            
        if url == None:
            return redirect('request_view')
        print(url, request.POST)
        if url[:4] != 'http':
            url = 'https://'+url
        try:
            stuff = requests.get(url, timeout=10)
        except:
            return redirect('request_view')
        return HttpResponse(content=stuff)
    return render(request, 'cards/req.html', context)

def getvocab(word):
    url = f'https://www.vocabulary.com/search?q={word}'
    r = requests.get(url)
    print(r)
    formatted_text = soup(r.text,'html.parser')
    short = formatted_text.findAll('p',{'class':'short'})
    longdef = formatted_text.findAll('p',{'class':'long'})
    try:   
        ret = (str(short[0]),str(longdef[0]))
    except:
        ret = ['<p>Sorry, the word you searched is not in this dictionary.</p>','']
    return ret


def wordview(request):
    context = {}
    if request.POST:
        url = request.POST.get('url',None)
        if url == None:
            return redirect("word_view")
        context['short'],context['long'] = getvocab(url)
    return render(request, 'cards/req.html', context)
