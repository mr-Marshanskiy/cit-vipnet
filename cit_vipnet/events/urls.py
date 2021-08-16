from django.urls import include, path

from . import views

urlpatterns = [
    path('orgs/<int:pk>/new_vpn/', views.CreateVpnView.as_view(), name='new_vpn'),
    path('orgs/delete/vpn/<int:pk>', views.OrgListVpnDeleteView.as_view(), name='delete_vpn_of_org'),
    path('orgs/delete/org/<int:pk>', views.OrganisationDeleteView.as_view(), name='delete_org'),
    path('orgs/<int:pk>/', views.OrganisationSingleView.as_view(), name='single_org'),

    path('orgs/', views.OrganisationListView.as_view(), name='orgs'),

    path('acts/<int:pk>/', views.LicenseSingleView.as_view(), name='single_act'),
    path('acts/', views.LicenseListView.as_view(), name='acts'),
    path('acts/delete/<int:pk>/', views.SingleLicenseDeleteView.as_view(), name='delete_act'),

    path('sellers/', views.DistributorListView.as_view(), name='sellers'),
    path('sellers/<int:pk>/', views.DistributorDetailView.as_view(), name='single_seller'),
    path('sellers/delete/', views.DistributorListForDeleteView.as_view(), name='deleting_list_sellers'),
    path('sellers/delete/<int:pk>/', views.DistributorDeleteView.as_view(), name='delete_seller'),

    path('devices/', views.DevicesListView.as_view(), name='devices'),
    path('devices/<int:pk>/', views.DevicesDetailView.as_view(), name='single_device'),
    path('devices/delete/', views.DeviceListForDeleteView.as_view(), name='deleting_list_devices'),
    path('devices/delete/<int:pk>/', views.DevicesDeleteView.as_view(), name='delete_device'),

    path('new/org/', views.CreateOrgView.as_view(), name='new_org'),
    path('', views.IndexListView.as_view(), name='index'),
]