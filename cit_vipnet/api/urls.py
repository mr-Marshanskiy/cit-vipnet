from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()


router.register('licenses', views.LicenseViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls)),

]