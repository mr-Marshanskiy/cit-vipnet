from turtle import mode
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Organisation(models.Model):
    org_inn = models.CharField(max_length=10, verbose_name=u"ИНН организации")
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
        return f"{self.org_inn}"


class Reglament(models.Model):
    reg_number = models.CharField(
        max_length=8,
        verbose_name=u"Регистрационный номер",
        blank=True,
        null=True,
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
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.reg_number}"


class Distributor(models.Model):
    org_name = models.CharField(
        max_length=35,
        verbose_name=u"Организация дистрибьютора"
    )
    address = models.CharField(
        max_length=50,
        verbose_name=u"Местоположение",
        blank=True,
        null=True,
    )
    def __str__(self):
        return f"{self.org_name}"
    

class KeyDevice(models.Model):
    type = models.CharField(
        max_length=35,
        verbose_name=u"Тип носителя"
    )
    def __str__(self):
        return f"{self.type}"
    

class License(models.Model):
    n_license = models.CharField(
        max_length=20,
        verbose_name=u"Номер акта П/П"
    )
    lic_date = models.DateField(
        verbose_name=u"Дата акта",
        blank=True,
        null=True,
    )
    distrib_org = models.ForeignKey(
        "Distributor",
        on_delete=models.SET_NULL,
        related_name="distruitors",
        verbose_name=u"Распространитель",
        blank=True,
        null=True,
    )
    ammount = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u"Количество лицензий", 
    )

    def __str__(self):
        return f"{self.n_license}"


class Event(models.Model): 
    organisation = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        related_name="reg_numbers",
        verbose_name=u"Организация",
    )
    keys_number = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u"Рег. номер СКИ",
    )
    keys_date = models.DateField(
        #auto_now_add=True,
        verbose_name=u"Дата выдачи СКИ",
    )
    device_name = models.ForeignKey(
        "KeyDevice",
        on_delete=models.SET_NULL,
        related_name="devices",
        blank=True,
        null=True,
        verbose_name=u"СКИ записана на",
    )
    device_id = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name=u"Серийный номер устройства",
    )
    license = models.ForeignKey(
        "License",
        on_delete=models.SET_NULL,
        related_name="license",
        blank=True,
        null=True,
        verbose_name=u"Акт П/П",
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=u"Примечание",
    )
    vpn_number = models.CharField(
        blank=True,
        null=True,
        max_length=10,
        verbose_name=u"Номер VPN",
    )

    class Meta:
        ordering = ['id']
