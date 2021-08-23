
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from events.models import Organisation, Vpn, Device, Distributor, License


class LicenseSerializer(serializers.ModelSerializer):
    #distributor = serializers.SlugRelatedField(
    #    read_only=True,
     #   slug_field='name'
  #  )
    class Meta:
        model = License
        fields = ('act', 'date', 'distributor', 'amount')
