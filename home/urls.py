from django.contrib import admin
from django.urls import path
from . import views

app_name="home"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('s/<str:id>/', views.specialization, name="specialization"),
    path('filter/', views.clinicFilter, name="filter"),
    path("search/", views.advancedSearch, name="search"),
    path('', views.index, name="index"),
]
