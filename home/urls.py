from django.contrib import admin
from django.urls import path
from . import views
from accounts.views import profile
app_name="home"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('s/<str:id>/', views.specialization, name="specialization"),
    path('s/<str:id>/doctors-goverments/', views.doctorsInGoverments, name="doctors-goverments"),
    path("<str:uuid>/", profile, name="profile"),
    path('', views.index, name="index"),
]
