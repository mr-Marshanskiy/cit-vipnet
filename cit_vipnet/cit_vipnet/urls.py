from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # импорт правил из приложения events
    path("", include("events.urls")),
    # импорт правил из приложения admin
    path("admin/", admin.site.urls),
] 