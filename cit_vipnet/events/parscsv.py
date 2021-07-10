from . import models

from datetime import datetime
import csv

filepath = r'E:\db44.csv'
filepath_write = r'E:\db5_new.csv'
arr1 = []
arr2 = []
max_coloumn = 22
dictionary = {}

class Record:
    def __init__(self, arr):
        self.reg_number = arr[0]
        self.reg_date = arr[1]
        self.org_net = arr[2]
        self.org_name = arr[3]
        self.org_city = arr[4]
        self.org_state = arr[5]
        self.org_inn = arr[6]
        self.org_street = arr[7]
        self.org_street_n = arr[8]
        self.org_phone = arr[9]
        self.org_contact = arr[10]
        self.org_vpn = arr[11]
        self.keys_number = arr[12]
        self.keys_date = arr[13]
        self.keys_device_name = arr[14]
        self.keys_device_id = arr[15]
        self.distr_name = arr[16]
        self.dist_number = arr[17]
        self.distr_date = arr[18]
        self.distr_ammount = arr[19]
        self.advance_info = arr[20]

    def __str__(self):
        return (f'{self.reg_number};'
                f'{self.reg_date};'
                f'{self.org_net};'
                f'{self.org_name};'
                f'{self.org_state};'
                f'{self.org_city};'
                f'{self.org_street};'
                f'{self.org_street_n};'
                f'{self.org_inn};'
                f'{self.org_contact};'
                f'{self.org_phone};'
                f'{self.org_vpn};'
                f'{self.keys_number};'
                f'{self.keys_date};'
                f'{self.keys_device_name};'
                f'{self.keys_device_id};'
                f'{self.distr_name};'
                f'{self.dist_number};'
                f'{self.distr_date};'
                f'{self.distr_ammount};'
                f'{self.advance_info}')


class Application:
    def __init__(self):
        self.records = []
        self.filepath = r'E:\db.csv'
        filepath_write = r'E:\db_new.csv'

    def add_record(self, rec):

        #self.records.append(rec)
        #last_rec = self.records[-1]

        if rec.reg_number + rec.org_inn + rec.org_vpn == '':
            return
        last_rec = self.records[-1]
        if rec.reg_number == '':
            rec.reg_number = last_rec.reg_number
            rec.reg_date = last_rec.reg_date 

        if rec.org_net == '':
            rec.org_net = last_rec.org_net

        if rec.inn == '':
            rec.org_name = last_rec.org_name
            rec.org_state = last_rec.org_state
            rec.org_city = last_rec.org_city
            rec.org_street = last_rec.org_street
            rec.org_street_n = last_rec.org_street_n
            rec.org_inn = last_rec.org_inn
            rec.org_contact = last_rec.org_contact
            rec.org_phone = last_rec.org_phone

        if rec.distr_name == '':
            rec.distr_name = last_rec.distr_name
            rec.dist_number = last_rec.dist_number
            rec.distr_date = last_rec.distr_date
            rec.distr_ammount = last_rec.distr_ammount



        if ((rec.keys_device_name == '')
            and (last_rec.keys_device_name.lower() == 'usb')):
            rec.keys_device_name = last_rec.keys_device_name
            rec.keys_device_id = last_rec.keys_device_id
            rec.keys_number = last_rec.keys_number
            rec.keys_date = last_rec.keys_date

    def create_dict(self):
        with open(filepath, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                cur_arr = row[0].split(';')
                self.add_record(Record(cur_arr))
        return


def org_add(app):
    for org_rec in app.records:
        if not Organisation.objects.filter(
            org_inn=org_rec.org_inn,
        ).exists():
            Organisation.objects.create(
                org_inn=org_rec.org_inn,
                org_name=org_rec.org_name,
                org_state=org_rec.org_state,
                org_city=org_rec.org_city,
                org_address=org_rec.org_address,
                org_phone=org_rec.org_phone,
                org_contact_employee=org_rec.org_contact
            )

        if not Reglament.objects.filter(
            reg_number=org_rec.reg_number
        ).exists():
            org_object = Organisation.objects.filter(
                org_inn=org_rec.org_inn,
            )[0]
            try:
                reg_date_convert = datetime.strptime(
                    org_rec.reg_date, '%d.%m.%Y'
                )
            except ValueError:
                reg_date_convert = datetime(2000, 1, 1)
            Reglament.objects.create(
                reg_number=org_rec.reg_number,
                reg_date=reg_date_convert,
                reg_organisation= org_object,
            )

        if not Distributor.objects.filter(
            org_name=org_rec.distr_name
        ).exists():
            Distributor.objects.create(
                org_name=org_rec.distr_name,
            )

        if not KeyDevice.objects.filter(
            type=org_rec.keys_device_name.lower()).exists():
            KeyDevice.objects.create(
                type=org_rec.keys_device_name.lower(),
            )

        if not License.objects.filter(
            n_license=org_rec.dist_number,
        ).exists():
            distributor = Distributor.objects.filter(
                org_name=org_rec.distr_name
            )[0]
            try:
                lic_date_convert = datetime.strptime(
                    org_rec.distr_date, '%d.%m.%Y'
                )
            except ValueError:
                lic_date_convert = datetime(2000, 1, 1)
            try:
                ammount_convert = int(
                    org_rec.distr_ammount.split(' ')[0]
                )
            except ValueError:
                ammount_convert = 0
            License.objects.create(
                n_license=org_rec.dist_number,
                lic_date=lic_date_convert,
                distrib_org=distributor,
                ammount=ammount_convert
            )

        try:
            keys_date_convert = datetime.strptime(
                org_rec.keys_date, '%d.%m.%Y'
            )
        except ValueError:
                keys_date_convert = datetime(2000, 1, 1)

        try:
            key_number = int(org_rec.keys_number)
        except ValueError:
            key_number = 0
        #if not Event.objects.filter(
        #    keys_number=key_number,
        #    vpn_number=org_rec.org_vpn,
        #).exists():
        organisation = Organisation.objects.filter(
            org_inn=org_rec.org_inn
        )[0]
        device =  KeyDevice.objects.filter(
            type=org_rec.keys_device_name.lower()
        )[0]
        Event.objects.create(
            organisation=organisation,
            keys_number=key_number,
            keys_date=keys_date_convert,
            device_name=device,
            device_id=org_rec.keys_device_id,
            license=License.objects.filter(
                n_license=org_rec.dist_number
            )[0],
            comment=org_rec.advance_info,
            vpn_number=org_rec.org_vpn,
        )


#dbtable = create_dict()
#org_add(dbtable)
#reglament_add(dbtable)
    