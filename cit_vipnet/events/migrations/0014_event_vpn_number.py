# Generated by Django 2.2.9 on 2020-12-17 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20201217_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='vpn_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Номер VPN'),
        ),
    ]
