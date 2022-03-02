from django.db import models
from django.urls import reverse
from user_profile.models import User
from django.utils.text import slugify
from.slugs import genaret_unique_slug
from ckeditor.fields import RichTextField


# Create your models here.


class Category(models.Model):
    title=models.CharField(max_length=150, unique=True)
    slug=models.SlugField(null=True, blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:category_blogs", args={
             self.slug
             })
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save (*args, **kwargs)



class Tags(models.Model):
    title=models.CharField(max_length=150)
    slug=models.SlugField(null=True, blank=True)
    created_date=models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super().save (*args, **kwargs)

    def get_tags_absolute_url(self):
        return reverse("blog:tags_blogs", args={
             self.slug
             })


class Blog (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_blogs')
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_blogs')
    tags=models.ManyToManyField(Tags, related_name='tags', blank=True)
    likes=models.ManyToManyField(User, related_name='user_likes', blank=True)
    title=models.CharField(max_length=250)
    
    slug=models.SlugField(null=True, blank=True)
    banner=models.ImageField(upload_to='banner-images/')
    description=RichTextField()
    created_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        updating=self.pk is not None
        if updating:
            self.slug=genaret_unique_slug(self, self.title, update=True)
            super().save (*args, **kwargs)
        else:           
            self.slug=genaret_unique_slug(self, self.title)
            super().save (*args, **kwargs)


    def get_absolute_url(self):
        return reverse("blog:blog_details", kwargs={
            "slug": self.slug
            })


class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    blog=models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    text=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
    
    
    
class Reply(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replies')
    text=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text