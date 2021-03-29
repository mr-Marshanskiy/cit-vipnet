# Generated by Django 2.2.9 on 2020-12-17 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20201217_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='license',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='license', to='events.License'),
        ),
    ]
