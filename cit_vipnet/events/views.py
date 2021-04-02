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
