from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

SIMPLE_AUTOCOMPLETE = {'events.organisation': {'search_field': 'inn'}}

class Distributor(models.Model):
    name = models.CharField(
        max_length=75,
        verbose_name=u'Дистрибьютор',)
    address = models.CharField(
        max_length=50,
        verbose_name=u'Местоположение',
        blank=True,
        null=True,)

    class Meta:
        verbose_name = 'Дистрибьютор'
        verbose_name_plural = 'Дистрибьюторы'

    def __str__(self):
        return f'{self.name}'


class Device(models.Model):
    type = models.CharField(
        max_length=35,
        verbose_name=u'Тип носителя')

    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    def __str__(self):
        return f'{self.type}'


class Network(models.Model):
    number = models.CharField(
        max_length=35,
        verbose_name=u'Номер сети')

    class Meta:
        verbose_name = 'Защищенная сеть'
        verbose_name_plural = 'Защищенные сети'

    def __str__(self):
        return f'{self.number}'


class Region(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name=u'Населенный пункт')

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

    def __str__(self):
        return f'{self.name}'


class Organisation(models.Model):
    reg_number = models.PositiveIntegerField(
        verbose_name=u'Регистрационный номер',
        blank=True,
        null=True,)
    reg_date = models.DateField(
        #auto_now_add=True,
        verbose_name=u'Дата присоединения к Регламенту',
        blank=True,
        null=True,)
    inn = models.CharField(max_length=10, verbose_name=u'ИНН')
    kpp = models.CharField(
        max_length=8,
        verbose_name=u'КПП',
        blank=True,
        null=True,)
    full_name = models.CharField(
        max_length=150,
        verbose_name=u'Полное название',
        blank=True,
        null=True,)
    short_name = models.CharField(
        max_length=75,
        verbose_name=u'Сокращенное название',
        blank=True,
        null=True,)
    town = models.ForeignKey(
        'Region',
        on_delete=models.SET_NULL,
        verbose_name=u'Населенный пункт',
        blank=True,
        null=True,)
    address = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=u'Адрес организации',)
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=u"Номер телефона",)
    employee = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=u'Ответственный за СКЗИ',)
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=u'Комментарий',)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['-reg_number']
    def __str__(self):
        return f'{self.inn}'


class License(models.Model):
    act = models.CharField(
        max_length=20,
        verbose_name=u'Номер акта П/П',)
    date = models.DateField(
        verbose_name=u'Дата акта',
        blank=True,
        null=True,)
    distributor = models.ForeignKey(
        'Distributor',
        on_delete=models.SET_NULL,
        related_name="distributors",
        verbose_name=u"Распространитель",
        blank=True,
        null=True,)
    amount = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u'Количество лицензий', )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=u'Комментарий',)

    class Meta:
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'

    def __str__(self):
        return f'{self.act}'


class Vpn(models.Model):
    network = models.ForeignKey(
        'Network',
        on_delete=models.SET_NULL,
        related_name='nets',
        blank=True,
        null=True,)
    reg_number = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name=u'Рег. номер СКИ',)
    reg_date = models.DateField(
        blank=True,
        null=True,
        #auto_now_add=True,
        verbose_name=u"Дата выдачи СКИ",)
    organisation = models.ForeignKey(
        'Organisation',
        on_delete=models.CASCADE,
        related_name='orgs',
        verbose_name=u'Организация',)
    vpn_number = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=u'Номер VPN',)
    device_type = models.ForeignKey(
        'Device',
        on_delete=models.SET_NULL,
        related_name='devices',
        blank=True,
        null=True,
        verbose_name=u'Тип носителя',)
    device_id = models.CharField(
        blank=True,
        null=True,
        max_length=30,
        verbose_name=u'Идентификатор устройства',)
    license = models.ForeignKey(
        'License',
        on_delete=models.SET_NULL,
        related_name='lics',
        blank=True,
        null=True,
        verbose_name=u'Акт П/П',)
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=u'Примечание',)
    active = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = 'Дистрибутив ключей'
        verbose_name_plural = 'Дистрибутивы ключей'
        ordering = ['-reg_date']

    def __str__(self):
        return f'{self.reg_number}'

