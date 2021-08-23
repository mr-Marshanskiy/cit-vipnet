from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet

from events.models import Organisation, Vpn, Device, Distributor, License
from .serializers import LicenseSerializer


class MixinAndViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):

    def get_object(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: self.kwargs[lookup_url_kwarg],
            **kwargs,
        }

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(user=self.request.user)
        success = instance.delete()
        return Response({'success': bool(success)}, status=HTTP_200_OK)


class LicenseViewSet(ListModelMixin, GenericViewSet):
    queryset = License.objects.all().select_related('distributor')
    serializer_class = LicenseSerializer
    filter_backends = (SearchFilter, )
    search_fields = ('act',)