from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    
    path('',views.index, name='home'),
    path('blog/',views.blog, name='blog'),
    path('category_blog/<slug>/',views.category_blogs, name='category_blogs'),
    path('tag_blog/<slug>/',views.tags_blogs, name='tags_blogs'),
    path('blog_details/<slug>/',views.blog_details, name='blog_details'),
    path('add_reply/<int:blog_id>/<int:comment_id>/',views.add_reply, name='add_reply'),
    path('like_blog/<int:pk>/',views.like_blog, name='like_blog' ),
    path('serch_blog/',views.search_blogs, name='search_blogs' ),
    path('my_blog/',views.my_blogs, name='my_blogs' ),
    path('add_blog/',views.add_blogs, name='add_blogs'),
    path('update_blog/<str:slug>/',views.update_blog, name='update_blog'),
]
