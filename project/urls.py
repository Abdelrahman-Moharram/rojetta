
from django.contrib import admin
from django.urls import path , include
from project import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',include('home.urls',namespace='home')),
    path('admin/', admin.site.urls),
    path('auth/',include('Auth.urls',namespace='Auth')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)