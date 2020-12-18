
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("followers", views.followers, name="followers"),

    #API Routes
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("likes/<int:post_id>", views.likes, name="likes"),
    path("count/<int:post_id>", views.count, name="count"),
    path("delete/<int:post_id>", views.delete, name="delete")
]
