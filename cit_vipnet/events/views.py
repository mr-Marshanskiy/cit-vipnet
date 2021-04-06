from django.db.models.fields import related
from django.db.models.query import prefetch_related_objects
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Organisation, Reglament
from itertools import chain
from django.db import connection


def index(request):

    page = Organisation.objects.all().prefetch_related(
        'reg_orgs',
        'reg_numbers'
    )
    
    return render(
        request,
        'index.html',
        {
            'page': page,
        }
     )


def events(request):
    
    page = Organisation.objects.all().prefetch_related(
        'reg_orgs',
        'reg_numbers'
    )
    
    print(page.query)
    return render(
        request,
        'events.html',
        {
            'page': page,
        }
     )

    
