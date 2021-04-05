from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Organisation, Reglament

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
    )[:100]
    
    page = Event.objects.all().select_related('organisation').prefetch_related(
        'reg_numbers'
    )[:100]

    return render(
        request,
        'events.html',
        {
            'page': page,
        }
     )

