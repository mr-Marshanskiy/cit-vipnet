from multiprocessing import Event
from django.contrib import admin
#from admin_auto_filters.filters import AutocompleteFilter
from .models import (
    KeyDevice, License, Organisation, Reglament,
    Distributor, License, Event,
)

#class OrganistationFilter(AutocompleteFilter):
#    title = 'Organistation' # display title
 #   field_name = 'reg_organisation' # name of the foreign key field

class OrganisationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "org_inn",
        "org_name",
        "org_state",
        "org_city",
        "org_address",
        "org_contact_employee",
        "org_phone",
    ) 
    search_fields = ("org_inn",) 
    empty_value_display = "-пусто-"

class ReglamentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reg_number",
        "reg_organisation",
        "reg_date",
    ) 
    search_fields = ("reg_number", "reg_organisation__org_inn",) 
    empty_value_display = "-пусто-"
   # list_filter = [OrganistationFilter] 

class DistributorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "org_name",
        "address",
    ) 
    empty_value_display = "-пусто-"

class KeyDeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
    ) 
    empty_value_display = "-пусто-"

class LicenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "n_license",
        "lic_date",
        "distrib_org",
        "ammount",
    ) 
    empty_value_display = "-пусто-"

class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "organisation",
        "vpn_number",
        "keys_number",
        "keys_date",
        "device_name",
        "device_id",
        "license",
        "comment",
    ) 
    empty_value_display = "-пусто-"
    search_fields = ("keys_number", "organisation__org_inn",) 

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Reglament, ReglamentAdmin)
admin.site.register(Distributor, DistributorAdmin)
admin.site.register(KeyDevice, KeyDeviceAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Event, EventAdmin)