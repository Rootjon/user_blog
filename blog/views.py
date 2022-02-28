from genericpath import exists
from turtle import title
from urllib.request import Request
from django.utils.text import slugify
from unicodedata import category
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from user_profile.models import User
from.models import Category, Tags, Blog, Comment, Reply
from.forms import TextForm, AddBlogForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def index (request):
    blogs=Blog.objects.order_by('-created_date')
    tags=Tags.objects.order_by('-created_date')
    context={
        'blogs':blogs,
        'tags':tags,
    }
    return render(request,'index.html',context)

def blog (request):
    blogs=Blog.objects.order_by('-created_date')
    tags=Tags.objects.order_by('-created_date')
    
    paginator=Paginator(blogs,4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context={
        'blogs':blogs,
        'tags':tags,
        'page_obj':page_obj,
    }
    
    return render(request,'blog.html',context)

def category_blogs(request, slug):
    category=get_object_or_404(Category, slug=slug)
    recent_post=Blog.objects.order_by('-created_date')[:4]
    blogs=category.category_blogs.all()
    tags=Tags.objects.order_by('-created_date')[:4]
    paginator=Paginator(blogs,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'blogs':blogs,
        'tags':tags,
        'page_obj':page_obj,
        'recent_post':recent_post,
    }
    return render(request,'category_blogs.html',context)


def tags_blogs(request, slug):
    tags=get_object_or_404(Tags, slug=slug)
    recent_post=Blog.objects.order_by('-created_date')[:4]
    blogs=tags.tags.all()
    tags=Tags.objects.order_by('-created_date')[:4]
    paginator=Paginator(blogs,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'blogs':blogs,
        'tags':tags,
        'page_obj':page_obj,
        'recent_post':recent_post,
    }
    return render(request,'tags_blog.html',context)

def blog_details(request, slug):
    form=TextForm()
    blog=get_object_or_404(Blog, slug=slug)
    recent_post=Blog.objects.order_by('-created_date')[:4]
    tags=Tags.objects.order_by('-created_date')[:4]
    category=Category.objects.get(id=blog.category.id)
    related_blogs=category.category_blogs.all()
    liked_by=request.user in blog.likes.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form=TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                blog=blog,   
                text=form.cleaned_data.get('text')
            )
            messages.success(request, 'Your comment submitted.')
            #return redirect('blog_details', slug=blog.slug)
            return HttpResponseRedirect(request.path_info)
    context={
        'blog':blog,
        'recent_post':recent_post,
        'tags':tags,
        'related_blogs':related_blogs,
        'form':form,
        'liked_by':liked_by
    }

    return render(request,'blog_details.html',context)

@login_required(login_url='user_profile:login')
def add_reply(request, blog_id, comment_id):
    blog=get_object_or_404(Blog, id=blog_id)  
    if request.method == 'POST':
        form=TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,  
                text=form.cleaned_data.get('text')
            )
            messages.success(request, 'Your comment submitted.')
            return redirect('blog:blog_details', slug=blog.slug)
    return redirect('blog:blog_details', slug=blog.slug)


@login_required(login_url='user_profile:login')
def like_blog(request, pk):
    context={}
    blog=get_object_or_404(Blog, pk=pk)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        context['liked'] =False
        context['like_count']= blog.likes.all().count()

    else:
        blog.likes.add(request.user)
        context['liked'] =True
        context['like_count']= blog.likes.all().count()

    return JsonResponse(context, safe=False)

def search_blogs(request):
    search_key =request.GET.get('search', None)
    tags=Tags.objects.order_by('-created_date')
    
    if search_key:
        blogs=Blog.objects.filter(
            Q(title__icontains=search_key) |
            Q(category__title__icontains=search_key) |
            Q(user__username__icontains=search_key) |
            Q(tags__title__icontains=search_key) |
            Q(description__icontains=search_key) 

        ).distinct()

        paginator=Paginator(blogs,4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={
            'blogs':blogs,
            'page_obj':page_obj,
            'tags':tags,
            'search_key':search_key,
        }
        return render(request,'search.html',context)

    else:
        #return redirect('blog:home')

        blogs=Blog.objects.order_by('-created_date')
        tags=Tags.objects.order_by('-created_date')

        paginator=Paginator(blogs,2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={
            'blogs':blogs,
            'page_obj':page_obj,
            'tags':tags,
        }
        return render(request,'search.html',context)
            

            
@login_required(login_url='user_profile:login')      
def my_blogs(request):
    queryset=request.user.user_blogs.all()
    paginator=Paginator(queryset,3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    delete=request.GET.get('delete', None)

    if delete:

        blog=get_object_or_404(Blog, pk=delete)

        if request.user.pk != blog.user.pk:
            return redirect('blog:home')
        blog.delete()
        messages.success(request, 'Your blog has been deleted')
        return redirect('blog:my_blogs')
    context={
        'queryset':queryset,
        'page_obj':page_obj,

    }
    return render(request,'my_blogs.html',context)  
    

@login_required(login_url='user_profile:login')      
def add_blogs(request):
    form = AddBlogForm()
    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES)
        if form.is_valid():
            tags=request.POST['tags'].split(',')
            user=get_object_or_404(User, pk=request.user.pk)
            category=get_object_or_404(Category, pk=request.POST['category'])
            blog=form.save(commit=False)
            blog.user=user
            blog.category=category
            blog.save()
            for tag in tags:
                tag_input = Tags.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t=tag_input.first()
                    blog.tags.add(t)
                else:
                    if tag != '':
                        new_tag=Tags.objects.create(
                        title=tag.strip(),
                        slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)
                    
            messages.success(request,'Blog Added successfully')
            return redirect('blog:blog_details', slug=blog.slug)

        else:
            print(form.errors)

    context={
        'form':form,
    }

    return render(request,'addblog.html',context) 

@login_required(login_url='user_profile:login')      
def update_blog(request, slug):
    form = AddBlogForm()
    blog=get_object_or_404(Blog, slug=slug)
    form = AddBlogForm(instance=blog)

    if request.method == 'POST':
        form = AddBlogForm(request.POST, request.FILES, instance=blog)

        if form.is_valid():

            if request.user.pk != blog.user.pk:
                return redirect ('blog:home')

            tags=request.POST['tags'].split(',')
            user=get_object_or_404(User, pk=request.user.pk)
            category=get_object_or_404(Category, pk=request.POST['category'])
            blog=form.save(commit=False)
            blog.user=user
            blog.category=category
            blog.save()
            for tag in tags:
                tag_input = Tags.objects.filter(
                    title__iexact=tag.strip(),
                    slug=slugify(tag.strip())
                )
                if tag_input.exists():
                    t=tag_input.first()
                    blog.tags.add(t)
                else:
                    if tag != '':
                        new_tag=Tags.objects.create(
                        title=tag.strip(),
                        slug=slugify(tag.strip())
                        )
                        blog.tags.add(new_tag)
                    
            messages.success(request,'Blog updated successfully')
            return redirect('blog:blog_details', slug=blog.slug)

        else:
            print(form.errors)

    context={
        'form':form,
        'blog':blog,
    }

    return render(request,'update_blog.html',context) 