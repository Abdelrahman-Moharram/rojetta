from django.contrib import admin
from django.urls import path
from .views import *
app_name="accounts"


urlpatterns = [
    path("login/", user_login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_user, name="logout"),
    path("add-doc/", addDocData, name="adddoc"),
    path("add-clinic/", addClinic, name="addClinic"),
    path("getStates/<str:name>/", getStates, name="getStates"),
    path("upgrade-account/", upgradeAccount, name="upgradeAccount"),
    path("<str:uuid>/", profile, name="profile"),
]
