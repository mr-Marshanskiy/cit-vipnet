from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.debug, name='debug'),
    path('add_org/', views.add_organisations, name='add_org'),
    path('add_distr/', views.add_distributors, name='add_distr'),
    path('add_lic/', views.add_licenses, name='add_lic'),
    path('move_device', views.move_device, name='move_device'),
    path('move_distributors', views.move_distributors, name='move_distributors'),
    path('add_vpn/', views.add_vpn, name='add_vpn'),
    path('add_devices/', views.add_devices, name='add_devices'),
    path('del_all_vpn/', views.del_all_vpn, name='del_all_vpn'),
    path('del_all_act/', views.del_all_act, name='del_all_act'),
    path('change_short_name/', views.change_short_name, name='change_short_name'),
    path('change_lics/', views.change_lics, name='change_lics'),
    path('unmerge_with_filling/', views.unmerge_with_filling, name='unmerge_with_filling'),
]