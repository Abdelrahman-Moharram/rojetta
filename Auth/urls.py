from django.contrib import admin
from django.urls import path
from .views import *
app_name="Auth"


urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_user, name="logout"),
    path("add-doc/", addDocData, name="adddoc"),
    
]
