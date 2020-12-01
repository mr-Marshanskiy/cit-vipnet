from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Organisation(models.Model):
    org_inn = models.CharField(max_length=6, verbose_name=u"ИНН организации")
    org_name = models.CharField(
        max_length=120,
        verbose_name=u"Название организации",
        )
    org_state = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=u"Муниципальный район/округ",
    )
    org_city = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=u"Населенный пункт",
    )
    org_address = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=u"Физический адрес",
    )
    org_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=u"Номер телефона",
    )
    org_contact_employee = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=u"Ответственный за СКЗИ",
    )
    org_comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} | {self.org_inn} | {self.org_name}"


class Reglament(models.Model):
    reg_number = models.CharField(
        max_length=6,
        verbose_name=u"Регистрационный номер"
    )
    reg_organisation = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        related_name="reg_orgs",
        verbose_name=u"Организация",
    )
    reg_date = models.DateField(
        #auto_now_add=True,
        verbose_name=u"Дата присоединения",
    )
'''
class Event(models.Model): 
    reg_number = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        related_name="reg_numbers"
    )
    keys_number = models.IntegerField(),
    keys_date = models.DateTimeField(
        "keys date",
        auto_now_add=True
    )
    device_name = models.ForeignKey(
        "Device",
        on_delete=models.SET_NULL,
        related_name="devices"
    )
    device_id = models.CharField(
        blank=True,
        null=True,
        max_length=30
    )
    dist_number = models.CharField(
        blank=True,
        null=True,
        max_length=30
    ) 
    comment = models.TextField(
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="authors"
    )
'''