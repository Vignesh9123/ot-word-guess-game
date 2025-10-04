from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("start_game", views.start_game, name="start_game"),
    path("play/<int:game_id>", views.play, name="play"),
    path("wordgame/admin/day", views.admin_day, name="admin_day"),
    path("wordgame/admin/user", views.admin_user, name="admin_user")
]