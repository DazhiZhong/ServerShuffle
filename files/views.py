from django.shortcuts import render, redirect
from .models import *
from .forms import *
import os
import random
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.views.generic import FormView


def upload_file(request):
    if request.method == "POST":
        form = FilePostForm(request.POST,request.FILES)
        
        if form.is_valid():
            form.save()
            
    else:
        form = FilePostForm()
    return render(request,'files/upload_file.html',{'title':'file','form':form})



def files(request):
    

    content = FilePost.objects.all()
    
    content = reversed(content)
    #ct = Post.objects.filter(id=37)
    #print(ct[0].id)
    #u = request.user
    #print(dir(u))
    return render(request,'files/files.html',{'title':'ass','cts':content})

