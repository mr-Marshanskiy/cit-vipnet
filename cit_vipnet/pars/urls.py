from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.debug, name='debug'),
    path('add_org/', views.add_organisations, name='add_org'),
    path('add_distr/', views.add_distributors, name='add_distr'),
    path('add_lic/', views.add_licenses, name='add_lic'),
    path('add_vpn/', views.add_vpn, name='add_vpn'),
    path('add_devices/', views.add_devices, name='add_devices'),
    path('del_all_vpn/', views.del_all_vpn, name='del_all_vpn'),
    path('change_short_name/', views.change_short_name, name='change_short_name'),
]