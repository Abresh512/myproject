from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_room, name="login"),
    path("logout/", views.logout_room, name="logout"),
    path("register/", views.register_room, name="register"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),

    path("", views.index, name="index"),
    path("room/<str:pk>/", views.room, name="room"),

    path("create_room", views.create_room, name="create_room"),
    path("userprofile/<str:pk>/", views.userProfile, name="user-profile"),

    path("update-room/<str:pk>/", views.updateroom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),

]