from django.contrib import admin

from .models import Organisation, Reglament

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
    search_fields = ("inn",) 
    list_filter = ("id", "org_state", "org_city") 


class ReglamentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reg_number",
        "reg_organisation",
        "reg_date",
    ) 
    #search_fields = ("inn",) 
    list_filter = ("id", "reg_number", "reg_date")

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Reglament, ReglamentAdmin)
