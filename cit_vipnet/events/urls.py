from django.urls import include, path

from . import views

urlpatterns = [
    path('orgs/<str:inn>/', views.single_org, name='single_org'),
    path('orgs/', views.orgs, name='orgs'),
    path('', views.index, name='index'),
    
    
] 