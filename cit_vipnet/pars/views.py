from django.shortcuts import render
from .parscsv2 import ParsXlsx
from events.models import Organisation, Vpn
def debug(request):
        #app = ParsXlsx()
        #app.add_organisations()
        page = Organisation.objects.all()
        return render(
        request,
        'debug.html',
     )

def add_organisations(request):
    app = ParsXlsx()
    logs = app.add_organisations()
    return render(
        request,
        'debug.html',
        {
            'message': 'Скрипт по добавлению организаций выполнен',
            'logs': logs,
        }
    )

def add_distributors(request):
    app = ParsXlsx()
    logs = app.add_distributors()
    return render(
        request,
        'debug.html',
        {
            'message': 'Скрипт по добавлению дистрибьюторов выполнен',
            'logs': logs,
        }
    )

def add_licenses(request):
    app = ParsXlsx()
    logs = app.add_licenses()
    return render(
        request,
        'debug.html',
        {
            'message': 'Скрипт по добавлению лицензий выполнен',
            'logs': logs,
        }
    )

def add_devices(request):
    app = ParsXlsx()
    logs = app.add_devices()
    return render(
        request,
        'debug.html',
        {
            'message': 'Скрипт по добавлению устройств выполнен',
            'logs': logs,
        }
    )


def add_vpn(request):
    app = ParsXlsx()
    logs = app.add_vpn()
    return render(
        request,
        'debug.html',
        {
            'message': 'Скрипт по добавлению СКИ выполнен',
            'logs': logs,
        }
    )

def del_all_vpn(request):
    Vpn.objects.all().delete()
    return render(
        request,
        'debug.html',
        {
            'message': 'Все СКИ были удалены',
        }
    )

def change_short_name(request):
    orgs = Organisation.objects.all()
    for org in orgs:
        new_name = org.short_name
        if 'Ставропольского края' in org.short_name:
            new_name = org.short_name.replace('Ставропольского края', 'СК')
        elif 'муниципального округа' in org.short_name:
            new_name = org.short_name.replace('муниципального округа', 'МО')
        elif 'муниципального района' in org.short_name:
            new_name = org.short_name.replace('муниципального района', 'МР')
        elif 'территориальный отдел' in org.short_name:
            new_name = org.short_name.replace('территориальный отдел', 'ТО')
        elif 'Государственное бюджетное учреждение' in org.short_name:
            new_name = org.short_name.replace('Государственное бюджетное учреждение', 'ГБУ')
        elif 'Муниципальное бюджетное дошкольное образовательное учреждение' in org.short_name:
            new_name = org.short_name.replace('Муниципальное бюджетное дошкольное образовательное учреждение', 'МБДОУ')
        if new_name != org.short_name:
            org.short_name = new_name
            org.save()

    return render(
        request,
        'debug.html',
        {
            'message': 'Операция сокращения выполнена',
        }
    )
