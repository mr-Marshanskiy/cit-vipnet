from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # импорт правил из приложения events
    path('inventory/', include('inventory.urls')),
    path("", include('events.urls')),

    # импорт правил из приложения admin
    path('admin/', admin.site.urls),
    path('debug/', include('pars.urls')),
    path('api/', include('api.urls'))
] 