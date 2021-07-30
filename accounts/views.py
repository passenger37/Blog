from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout
from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import Login, SignUp,ProfileForm
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.core.paginator import Paginator

def register(request):
    signup_form=SignUp(auto_id='form_%s',label_suffix="")
    if request.method=="POST":
        signup_form=SignUp(request.POST)
        if signup_form.is_valid():
            new_user=signup_form.save()
            authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
            if authenticated_user is not None:
                login(request,authenticated_user)
                messages.success(request,'Welcome  {user}'.format(user=new_user))
                return HttpResponseRedirect(reverse('topic:index'))
    context={
        'signup':signup_form,
    }
    return render(request,"accounts/signup.html",context)

def login_form(request):
    login_form=Login(data=request.POST or None,auto_id="form_%s",label_suffix="")
    if request.method=="POST":
        login_form=Login(request=request,data=request.POST)
        if login_form.is_valid():
            uname=login_form.cleaned_data['username']
            upass=login_form.cleaned_data['password']
            user=authenticate(username=uname ,password=upass)
            if user.is_authenticated:         
                login(request,user)
                messages.success(request,'Welcome back {user}'.format(user=user))
                return HttpResponseRedirect(reverse('topic:index')) 
    context={
        'login':login_form,
    }
    return render(request,"accounts/login.html",context)


def logout_form(request):
    messages.success(request,'Successfully  Logout  {user}'.format(user=request.user))
    logout(request)
    return HttpResponseRedirect(reverse('topic:index'))


def profile(request,id):
    profile_user=Profile.objects.get(id=id)
    page_obj=Paginator(profile_user, 2)
    print(">>>>>>>>>>>>>>>> PAGE OBJECT ",page_obj)
    context={
        'profile_user':profile_user,
        'page':page_obj,}
    return render(request,'accounts/profile.html',context)

# @login_required
def show_profile(request):
    profile_user=Profile.objects.get(user=request.user)
    if request.method=='POST':
        user_form=SignUp(request.POST,instance=request.user,prefix='signup_form')
        profile_form=ProfileForm(request.POST,request.FILES,instance=request.user.profile,prefix='profile_form')
        print(user_form)
        print(profile_form)
        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile Saved !! ')
            HttpResponseRedirect(reverse('topic:index'))
    user_form=SignUp(instance=request.user,prefix='signup_form')
    profile_form=ProfileForm(instance=request.user.profile,prefix='profile_form')
    context={
        'profile_form':profile_form,
        'user_form':user_form,
        'profile_user':profile_user
        }
    return render(request,'accounts/show_profile.html',context)