from django.contrib import admin
from django.urls import path
from . import views
from accounts.views import profile
app_name="home"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path("<str:uuid>/", profile, name="profile"),
]
