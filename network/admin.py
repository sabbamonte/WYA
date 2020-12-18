from django.contrib import admin
from .models import User, New_Post, Following, Avatar

# Register your models here.
admin.site.register(User)
admin.site.register(New_Post)
admin.site.register(Following)
admin.site.register(Avatar)