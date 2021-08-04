from django.shortcuts import render
from .parscsv2 import ParsXlsx
from events.models import Organisation, Vpn, License, Device, Distributor

from .forms import MoveDeviceForm, MoveDistributorForm


def debug(request):
        form = MoveDeviceForm()

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

def del_all_act(request):
    License.objects.all().delete()
    return render(
        request,
        'debug.html',
        {
            'message': 'Все Акты были удалены',
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


def change_lics(request):
    lics = License.objects.all().prefetch_related()
    for lic in lics:
        try:
            new_lic_act = str(lic.act.split(' ')[-1])
        except:
            new_lic_act = lic.act
        if new_lic_act.isnumeric():
            old_act = lic.act
            try:
                lic.act = new_lic_act
                lic.save()
            except:
                unique_lic = lics.get(act=new_lic_act)
                vpn = lic.lics.filter(act=old_act)
                for key in vpn:
                    key.license = unique_lic
                    key.save()
                lic.delete()
    
    return render(
        request,
        'debug.html',
        {
            'message': 'Операция преобразования актов выполнена',
        }
    )

def unmerge_with_filling(request):
    app = ParsXlsx()
    app.unmerge_with_filling()
    app.save_new_xlsx()
    return render(
        request,
        'debug.html',
        {
            'message': 'Скрипт по заполнению таблицы выполнен',
        }
    )


def move_device(request):
    if request.method != 'POST':
        form = MoveDeviceForm()
        return render(
            request, 
            'debug.html',
            {
            'form': form,
            }
        )
    
    form = MoveDeviceForm(request.POST)
    try:
        old_type = form['old_type'].value()
        new_type = form['new_type'].value()

        old_device = Device.objects.get(id=old_type)
        new_device = Device.objects.get(id=new_type)
    except:
        return render(
            request,
            'debug.html',
            {
                'message': f'Проверьте введенные данные',
                'form': form,
            }
        )
    if old_device == new_device:
        return render(
        request,
        'debug.html',
        {
            'message': f'{old_type} и {new_type} как бы одинаковы?!?!?',
            'form': form,
        }
    )

    vpn = Vpn.objects.filter(device_type=old_device)

    for key in vpn:
        key.device_type = new_device
        key.save()
    
    old_device.delete()
    
    form = MoveDeviceForm()
    return render(
        request,
        'debug.html',
        {
            'form':form,
            'message': f'Слияние актов произведено',
        }
    )


def move_distributors(request):
    if request.method != 'POST':
        form = MoveDistributorForm()
        return render(
            request, 
            'debug.html',
            {
            'form_move_distr': form,
            }
        )
    
    form = MoveDistributorForm(request.POST)
    try:
        old_seller_id = form['old_seller'].value()
        new_seller_id = form['new_seller'].value()

        old_seller = Distributor.objects.get(id=old_seller_id)
        new_seller = Distributor.objects.get(id=new_seller_id)
    except:
        return render(
            request,
            'debug.html',
            {
                'message': f'Проверьте введенные данные',
                'form_move_distr': form,
            }
        )
    if old_seller == new_seller:
        return render(
        request,
        'debug.html',
        {
            'message': f'{old_seller} и {new_seller} как бы одинаковы?!?!?',
            'form_move_distr': form,
        }
    )

    licenses = License.objects.filter(distributor=old_seller)

    for lic in licenses:
        lic.distributor = new_seller
        lic.save()
    
    old_seller.delete()
    
    form = MoveDistributorForm()
    return render(
        request,
        'debug.html',
        {
            'form_move_distr': form,
            'message': f'Слияние актов произведено',
        }
    )