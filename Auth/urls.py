from django.contrib import admin
from django.urls import path
from .views import *
app_name="Auth"


urlpatterns = [
    path("login/", user_login, name="login")
]
