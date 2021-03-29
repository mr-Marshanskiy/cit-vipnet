from django.urls import path

from .import views

urlpatterns = [
    path('', views.new, name='new'),
    path('organisation/', views.new_organisation, name='organisation'),
    path('reglament/', views.new_reglament, name='reglament'),
    path('license/', views.new_license, name='license'),
    path('event/', views.new_event, name='event'),
] 