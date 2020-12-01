from django.http import HttpResponse
from .parscsv import  create_dict
from .models import Organisation, Reglament

def org_add(app):
    for org_rec in app.records:
        if Organisation.objects.filter(org_inn=org_rec.org_inn).count() == 0:
            Organisation.objects.create(
                org_inn=org_rec.org_inn,
                org_name=org_rec.org_name,
                org_state=org_rec.org_state,
                org_city=org_rec.org_city,
                org_address=org_rec.org_address,
                org_phone=org_rec.org_phone,
                org_contact_employee=org_rec.org_contact
            )
     

def index(request):
    dbtable = create_dict()
    #add_rec(dbtable)

    latest = Organisation.objects.order_by('id')[:10]
    output = []
    for item in latest:
        output.append(item.org_inn)
    

    return HttpResponse('<'.join(output)) 
