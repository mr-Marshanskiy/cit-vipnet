from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrganisationForm


def new(request):
    return render(request,'new.html')


def new_organisation(request):
    if request.method != 'POST':
        form = OrganisationForm()
        return render(request, 'new/organisation.html', {'form': form})
    form = OrganisationForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(request, 'new/organisation.html', {'form': form})
    organisation = form.save(commit=False)
    organisation.save()
    return redirect('new')

def new_reglament(request):
    return render(request,'new.html')

def new_license(request):
    return render(request,'new.html')

def new_event(request):
    return render(request,'new.html')
