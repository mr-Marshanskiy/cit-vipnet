from django.shortcuts import render, get_object_or_404, redirect
from .models import Event


def index(request):
    page = Event.objects.all().select_related() 

    return render(
        request,
        'index.html',
        {
            'page': page,
        }
     )
