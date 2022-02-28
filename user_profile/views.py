from email.mime import image
from importlib.metadata import requires
import re
from urllib import request
from venv import create
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import is_valid_path
from.forms import UserRegistrationForm,LoginForm,UserProfileUpdateForm,ProfilePictureUpdatedForm
from django.contrib.auth import login, logout, authenticate
from.decorators import not_logged_in_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from.models import Follow, User
from notification.models import Notification

# Create your views here.
@never_cache
@not_logged_in_required
def login_user(request):
    form=LoginForm()
    if  request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('blog:home')
            else:
                messages.warning(request, 'Wrong credentials')
    context={
        'form':form,
    }

    return render(request,'login.html',context)

def logout_user(request):
    logout(request)
    return redirect('user_profile:login')

    

@never_cache
@not_logged_in_required
def register_user(request):
    form=UserRegistrationForm()
    if  request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, 'Registration successfull')
            return redirect('user_profile:login')


    context={
        'form':form,
    }

    return render(request,'registration.html',context)
@login_required(login_url='user_profile:login')
def profile(request):
    account = get_object_or_404(User, pk=request.user.pk)
    form=UserProfileUpdateForm(instance=account)
    if request.method == 'POST':
        if request.user.pk !=account.pk:
            return redirect('blog:home')
        form=UserProfileUpdateForm(request. POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile has been successfully updated')
            return redirect('user_profile:profile')
    context={
        'account':account,
        'form':form,
    }

    return render(request,'profile.html',context)

@login_required
def change_profile_picture(request):
    if request.method == 'POST':
        form=ProfilePictureUpdatedForm(request.POST, request.FILES)
        if form.is_valid():
            image=request.FILES['profile_image']
            user=get_object_or_404(User, pk=request.user.pk)
            if request.user.pk != user.pk:
                return redirect('blog:home')

            user.profile_image=image
            user.save()
            messages.success(request, 'Profile images updated successfully')
            return redirect('user_profile:profile')
    return redirect('user_profile:profile')

@login_required(login_url='user_profile:login')
def user_information(request, username):
    account=get_object_or_404(User, username=username)   
    following=False
    muted=None
    if request.user.is_authenticated:
        if request.user.id == account.id:
            return redirect('user_profile:profile')
        followers=account.followers.filter(
        followed_by__id = request.user.id
        )
        if followers.exists():
            following=True
    if following:
        queryset =followers.first()
        if queryset.muted:
            muted=True
        else:
            muted=False

    context={
        'account':account,
        'following':following,
        'muted':muted
    }
    return render(request,'user_information.html',context)  

@login_required(login_url='user_profile:login')
def follow_or_unfollow_user(request, user_id):
    followed=get_object_or_404(User, id=user_id)
    followed_by=get_object_or_404(User, id=request.user.id)

    follow, created =Follow.objects.get_or_create(
        followed=followed,
        followed_by=followed_by
    )

    if created:
        followed.followers.add(follow)

    else:
        followed.followers.remove(follow)
        follow.delete()  

    return redirect('user_profile:user_information', username = followed.username)

@login_required(login_url='user_profile:login')
def user_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user,
        is_seen=False
    )

    for notification in notifications:
        notification.is_seen = True
        notification.save()
        
    return render(request, 'notification.html')  

@login_required(login_url='user_profile:login')
def mute_or_unmute_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    follower = get_object_or_404(User, pk=request.user.pk)
    instance=get_object_or_404(

        Follow,
        followed=user,
        followed_by=follower
    )

    if instance.muted:
        instance.muted = False
        instance.save()

    else:
        instance.muted = True
        instance.save() 

    return redirect('user_profile:user_information', username=user.username)

