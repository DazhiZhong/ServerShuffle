from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegForm,ProfileForm, ImageForm, UserUpdateForm
from .models import Profile
from django.contrib import messages

# Create your views here.

@login_required
def register(request):


    if request.method == 'POST':
        form = UserRegForm(request.POST)
        print('ass')
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(username)

            

            messages.success(request,f'created for{username}')
            return redirect('cards_see')
    else:
        form = UserRegForm()
    
    return render(request,'register.html',{'form':form})
    
@login_required
def profile(request):

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        print('ass')
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            # we can have this be commented because we have a django signals that 
            # saves the post whenever we save a user
            # prof_form.save()
            messages.success(request,f'success in saving profile')
            return redirect('blog_profile')
            
    else:
        user_form = UserUpdateForm(instance=request.user)
        prof_form = ProfileForm(instance=request.user.profile)
    
    # user_form = UserUpdateForm(instance=request.user)
    # prof_form = ProfileForm(instance=request.user.profile)

    return render(request,'profile.html',{'user_form':user_form,'prof_form':prof_form})

@login_required
def newprofile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)

        if form.is_valid():
            print(request.FILES)
            form.save()
            return redirect('tprofile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request,'newprofile.html',{'form':form})