from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # NOTES APP URLS (TÜM ROUTELAR BURADAN GELİR)
    path('', include('notes.urls')),
]
