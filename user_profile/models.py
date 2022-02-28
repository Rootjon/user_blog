from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from .managers import CustomeUserManagers

# Create your models here.

class User(AbstractUser):
    email=models.EmailField(
        max_length=150,
        unique=True,
        error_messages={
            "unique":"The email must be uniqe"
        }
    )
    profile_image=models.ImageField(
        null=True,
        blank=True,
        upload_to='profile_image/'
                                    
    )
    followers = models.ManyToManyField('Follow')
    REQUIRED_FIELDS=["email"]
    objects= CustomeUserManagers()
    
    def __str__(self):
        return self.username


    def get_profile_piture(self):
        url = ""
        try:
            url=self.profile_image.url
        except:
            url = ""
        return url

class Follow(models.Model):
    followed=models.ForeignKey(User, related_name='user_followers', on_delete=models.CASCADE)
    followed_by=models.ForeignKey(User, related_name='user_follows', on_delete=models.CASCADE)
    muted=models.BooleanField(default=False)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.followed_by.username} started following {self.followed.username} "