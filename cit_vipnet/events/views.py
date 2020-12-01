from django.http import HttpResponse
from .parscsv import  create_dict
from .models import Organisation, Reglament

from datetime import datetime

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

def reglament_add(app):
    for org_rec in app.records:
        if Reglament.objects.filter(reg_number=org_rec.reg_number).count() == 0:
            org_object = Organisation.objects.filter(org_inn=org_rec.org_inn)[0]
            try:
                reg_date_convert = datetime.strptime(org_rec.reg_date, "%d.%m.%Y")
            except ValueError:
                reg_date_convert = datetime(2000, 1, 1)
            Reglament.objects.create(
                reg_number=org_rec.reg_number,
                reg_date=reg_date_convert,
                reg_organisation= org_object,
            )    

def index(request):
    dbtable = create_dict()
    #add_rec(dbtable)
    #reglament_add(dbtable)
    latest = Organisation.objects.order_by('id')[:10]
    output = []
    for item in latest:
        output.append(item.org_inn)
    

    return HttpResponse('<'.join(output)) 
