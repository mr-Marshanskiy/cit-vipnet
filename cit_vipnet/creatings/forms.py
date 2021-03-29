from django import forms
from events.models import Organisation
from django.utils.translation import gettext_lazy as _

class OrganisationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text

    class Meta:
        model = Organisation
        fields = (
            'org_inn',
            'org_name',
            'org_state',
            'org_city',
            'org_address',
            'org_phone',
            'org_contact_employee',
            'org_comment',
        )
        labels = {
            'org_inn': _('ИНН организации'),
            'org_name': _('Название организации'),
            'org_state': _('Район/Округ'),
            'org_city': _('Населенный пункт'),
            'org_address': _('Адрес'),
            'org_phone': _('Номер ответственного'),
            'org_contact_employee': _('ФИО Ответственного'),
            'org_comment': _('Комментарий'),
        }
        help_texts = {
            'org_inn': _('26226248'),
            'org_name': _('ГКУ СК "Краевой центр инфортехнологий"'),
            'org_state': _('г. Ставрополь / Петровский ГО'),
            'org_city': _('г. Ставрополь / с. Невидимка'),
            'org_address': _('ул. Ленина, д. 43'),
            'org_phone': _('+7(905)315-32-15'),
            'org_contact_employee': _('Иванов Иван Иванович'),
            'org_comment': _('Примечание к организации'),
        }