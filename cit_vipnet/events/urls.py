from django.urls import include, path

from . import views

urlpatterns = [
    path('orgs/', views.OrganisationListView.as_view(), name='orgs'),
    path('orgs/new/', views.OrganisationCreateView.as_view(), name='new_org'),
    path('orgs/<int:pk>/', views.OrganisationSingleView.as_view(), name='single_org'),
    path('orgs/<int:pk>/update_org/', views.OrganisationUpdateView.as_view(), name='update_org'),
    path('orgs/<int:pk>/delete_org/', views.OrganisationDeleteView.as_view(), name='delete_org'),
    path('orgs/<int:pk>/new_vpn/', views.VpnCreateView.as_view(), name='new_vpn'),
    path('orgs/<int:pk>/update_vpn/', views.VpnUpdateView.as_view(), name='update_vpn'),
    path('orgs/<int:pk>/delete_vpn/', views.OrgListVpnDeleteView.as_view(), name='delete_vpn_of_org'),

    path('acts/', views.LicenseListView.as_view(), name='acts'),
    path('acts/<int:pk>/', views.LicenseSingleView.as_view(), name='single_act'),
    path('acts/<int:pk>/update/', views.LicenseUpdateView.as_view(), name='update_act'),
    path('acts/<int:pk>/delete/', views.LicenseSingleDeleteView.as_view(), name='delete_act'),

    path('sellers/', views.DistributorListView.as_view(), name='sellers'),
    path('sellers/delete/', views.DistributorListForDeleteView.as_view(), name='deleting_list_sellers'),
    path('sellers/<int:pk>/', views.DistributorDetailView.as_view(), name='single_seller'),
    path('sellers/<int:pk>/delete/', views.DistributorDeleteView.as_view(), name='delete_seller'),

    path('devices/', views.DevicesListView.as_view(), name='devices'),
    path('devices/delete/', views.DeviceListForDeleteView.as_view(), name='deleting_list_devices'),
    path('devices/<int:pk>/', views.DevicesDetailView.as_view(), name='single_device'),
    path('devices/<int:pk>/delete/', views.DevicesDeleteView.as_view(), name='delete_device'),

    path('', views.IndexListView.as_view(), name='index'),
]