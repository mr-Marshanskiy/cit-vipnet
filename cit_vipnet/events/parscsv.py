from .models import Organisation

import csv

filepath = r"E:\db4.csv"
filepath_write = r"E:\db5_new.csv"
arr1 = []
arr2 = []
max_coloumn = 22
dictionary = {}

class Record:
    def __init__(self,arr):

        self.reg_number = arr[0]
        self.reg_date = arr[1]
        self.org_net = arr[2]
        self.org_name = arr[3]
        self.org_state = arr[5]
        self.org_city = arr[4]
        if arr[7] == "" and arr[8] == "":
            self.org_address = ""
        else:
            self.org_address = f"{arr[7]}, {arr[8]}"
        self.org_inn = arr[6]
        self.org_contact = arr[10]
        self.org_phone = arr[9]
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
        return (f"{self.reg_number};"
                f"{self.reg_date};"
                f"{self.org_net};"
                f"{self.org_name};"
                f"{self.org_state};"
                f"{self.org_city};"
                f"{self.org_address};"
                f"{self.org_inn};"
                f"{self.org_contact};"
                f"{self.org_phone};"
                f"{self.org_vpn};"
                f"{self.keys_number};"
                f"{self.keys_date};"
                f"{self.keys_device_name};"
                f"{self.keys_device_id};"
                f"{self.distr_name};"
                f"{self.dist_number};"
                f"{self.distr_date};"
                f"{self.distr_ammount};"
                f"{self.advance_info}")
                

class Application:
    def __init__(self):
        self.records = []
        
    def add_record(self, record):
        self.records.append(record)
        last_rec = self.records[-1]
        if last_rec.reg_number == "":
            last_rec.reg_number = self.records[-2].reg_number 
        else:
            return
        prev_rec = self.records[-2]
        if last_rec.reg_date == "":
            last_rec.reg_date = prev_rec.reg_date
        if last_rec.org_net == "":
            last_rec.org_net = prev_rec.org_net
        if last_rec.org_name == "":
            last_rec.org_name = prev_rec.org_name
        if last_rec.org_state == "":
            last_rec.org_state = prev_rec.org_state
        if last_rec.org_city == "":
            last_rec.org_city = prev_rec.org_city
        if last_rec.org_address == "":
            last_rec.org_address = prev_rec.org_address
        if last_rec.org_inn == "":
            last_rec.org_inn = prev_rec.org_inn
        if last_rec.org_contact == "":
            last_rec.org_contact = prev_rec.org_contact
        if last_rec.org_phone == "":
            last_rec.org_phone = prev_rec.org_phone
        if last_rec.distr_name == "":
            last_rec.distr_name = prev_rec.distr_name
        if last_rec.dist_number == "":
            last_rec.dist_number = prev_rec.dist_number
        if last_rec.distr_date == "":
            last_rec.distr_date = prev_rec.distr_date
        if last_rec.distr_ammount == "":
            last_rec.distr_ammount = prev_rec.distr_ammount
        if ((last_rec.keys_device_name == "") 
            and (prev_rec.keys_device_name in ["USB", "usb", "Usb"])):
            last_rec.keys_device_name = prev_rec.keys_device_name
            last_rec.keys_device_id = prev_rec.keys_device_id
            last_rec.keys_number = prev_rec.keys_number
            last_rec.keys_date = prev_rec.keys_date



def create_dict():
    app = Application()
    with open(filepath, encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cur_arr = row[0].split(';')
            app.add_record(Record(cur_arr))

    return app


    
            
    