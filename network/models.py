from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class New_Post(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="posts")
    post = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.ManyToManyField(User, default=None, null=True, blank=True, related_name="all_likes")
    counter = models.IntegerField(null=True)
        
    def serialize(self):
        return {
            "user": self.user,
            "post": self.post,
            "timestamp": self.timestamp,
            "likes":self.likes,
            "counter": self.counter
        }

class Following(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name="current_user")
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers", blank=True, default=None, null=True)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following", blank=True, default=None, null=True)

    def __str__(self):
        return f"User:{self.user} follows {self.following} and {self.followers} follow him/her."

class Avatar(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    avatar = models.ImageField(upload_to='images')

   



