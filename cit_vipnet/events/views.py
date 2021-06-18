from django.db.models.fields import related
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Organisation, Reglament


def index(request):

    page = Event.objects.select_related(
        'organisation'
    ).prefetch_related()
    return render(
        request,
        'index.html',
        {
            'page': page,
        }
     )

    

def events(request):
    
    page = Event.objects.all().select_related()
    
    page1 = Reglament.objects.all().select_related()

    print(page.query)
    print(page1.query)
    return render(
        request,
        'events.html',
        {
            'page': page,
        }
     )

    
