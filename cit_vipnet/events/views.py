from django.db.models.fields import related
from django.shortcuts import render, get_object_or_404, redirect
from .models import Vpn


def index(request):

    page = Vpn.objects.select_related(
        'organisation'
    ).prefetch_related()
    return render(
        request,
        'index.html',
        {
            'page': page,
        }
     )
