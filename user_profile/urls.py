from django.urls import path
from . import views


app_name = 'user_profile'

urlpatterns = [
   
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('registration/',views.register_user,name='register_user'),
    path('profile/',views.profile,name='profile'),
    path('profile_picture/',views.change_profile_picture,name='profile_picture'),
    path('user_information/<str:username>/',views.user_information,name='user_information'),
    path('follow_or_unfollow/<int:user_id>/',views.follow_or_unfollow_user,name='follow_or_unfollow_user'),
    path('notification/',views.user_notifications,name='user_notification'),
    path('mute_or_unmute_user/<int:user_id>/',views.mute_or_unmute_user,name='mute_or_unmute_user'),
]
