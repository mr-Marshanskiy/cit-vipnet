from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/',  views.events, name='events'),
    path('org/<str:inn>/', views.org_single, name='org_single'),
    path('licenses/', views.licenses, name='licenses'),
] 