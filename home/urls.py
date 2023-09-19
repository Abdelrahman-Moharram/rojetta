from django.contrib import admin
from django.urls import path
from . import views

app_name="home"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('s/<str:id>/', views.specialization, name="specialization"),
    path('doctors-goverments/', views.doctorsInGoverments, name="doctors-goverments"),
    path("search/", views.advancedSearch, name="search"),
    path('', views.index, name="index"),
]
