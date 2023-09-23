from django.contrib import admin
from django.urls import path
from . import views

app_name="clinic"


urlpatterns = [
    path('<int:id>/', views.clinic, name="browse"),
    path('manage', views.manage_clinic, name="manage"),

]