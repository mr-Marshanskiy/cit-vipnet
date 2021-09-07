from django.db import models


class Network(models.Model):
    number = models.CharField(
        max_length=35,
        verbose_name=u'Номер сети')

    class Meta:
        verbose_name = 'Защищенная сеть'
        verbose_name_plural = 'Защищенные сети'

    def __str__(self):
        return f'{self.number}'


class HardwarePlatform(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name=u'Аппаратная платформа')

    class Meta:
        verbose_name = 'Аппаратная платформа'
        verbose_name_plural = 'Аппаратные платформы'
        ordering = ['-name']

    def __str__(self):
        return f'{self.name}'


class Modification(models.Model):
    name = models.CharField(
        max_length=35,
        verbose_name=u'Модификация исполненеия')

    class Meta:
        verbose_name = 'Модификация исполненеия'
        verbose_name_plural = 'Модификации исполненеий'
        ordering = ['-name']

    def __str__(self):
        return f'{self.name}'


class Coordinator(models.Model):
    network = models.ForeignKey(
        'Network',
        on_delete=models.SET_NULL,
        related_name='coord',
        verbose_name=u'Защищенная сеть',
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=50,
        verbose_name=u'Название узла',)
    date = models.DateField(
        verbose_name=u'Дата введения в эксплуатацию',
        blank=True,
        null=True,)
    address = models.CharField(
        max_length=50,
        verbose_name=u'Местоположение',
        blank=True,
        null=True,
    )
    vipnet_id = models.CharField(
        max_length=10,
        verbose_name=u'Идентификатор в сети',
        blank=True,
        null=True,
    )
    modification = models.ForeignKey(
        'Modification',
        on_delete=models.SET_NULL,
        verbose_name=u'Модификация исполненеия',
        blank=True,
        null=True,
    )
    hardware_platform = models.ForeignKey(
        'HardwarePlatform',
        on_delete=models.SET_NULL,
        verbose_name=u'Аппаратная платформа',
        blank=True,
        null=True,
    )
    serial_number = models.CharField(
        max_length=25,
        verbose_name=u'Серийный номер',
        blank=True,
        null=True,
    )
    account_number_skzi = models.CharField(
        max_length=25,
        verbose_name=u'Учетный номер СКЗИ',
        blank=True,
        null=True,
    )
    account_number_fstec = models.CharField(
        max_length=25,
        verbose_name=u'Учетный номер ФСТЭК',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Координатор'
        verbose_name_plural = 'Координаторы'

    def __str__(self):
        return f'{self.name}'
