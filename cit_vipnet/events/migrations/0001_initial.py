# Generated by Django 2.2 on 2020-12-01 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_inn', models.CharField(max_length=6)),
                ('org_name', models.CharField(max_length=120)),
                ('org_address', models.CharField(blank=True, max_length=100, null=True)),
                ('org_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('org_contact_employee', models.CharField(blank=True, max_length=30, null=True)),
                ('org_comment', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
