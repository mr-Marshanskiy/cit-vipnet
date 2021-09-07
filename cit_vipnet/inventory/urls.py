from django.urls import include, path

from . import views


urlpatterns = [
    path('coords/', views.CoordListView.as_view(), name='coords'),
    path('coords/new/', views.CoordCreateView.as_view(), name='new_coord'),
    path('coords/<int:pk>/', views.CoordDetailView.as_view(), name='single_coord'),
    path('coords/<int:pk>/update/', views.CoordUpdateView.as_view(), name='update_coord'),
    path('coords/<int:pk>/delete/', views.CoordDeleteView.as_view(), name='delete_coord'),
]