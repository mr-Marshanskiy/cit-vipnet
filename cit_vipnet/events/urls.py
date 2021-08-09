from django.urls import include, path

from . import views

urlpatterns = [
    path('orgs/<str:inn>/', views.single_org, name='single_org'),
    path('orgs/', views.orgs, name='orgs'),
    path('acts/<int:pk>/', views.single_act, name='single_act'),
    path('acts/', views.acts, name='acts'),

    path('sellers/', views.DistributorListView.as_view(), name='sellers'),
    path('sellers/<int:pk>/', views.DistributorDetailView.as_view(), name='single_seller'),

    path('sellers/delete/', views.DistributorListForDeleteView.as_view(), name='deleting_list_sellers'),
    path('sellers/delete/<int:pk>/', views.DistributorDeleteView.as_view(), name='delete_seller'),

    path('devices/', views.DevicesListView.as_view(), name='devices'),
    path('devices/<int:pk>/', views.DevicesDetailView.as_view(), name='single_device'),
    
    path('', views.index, name='index'),

] 