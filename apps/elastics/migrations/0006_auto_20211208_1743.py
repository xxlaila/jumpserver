# Generated by Django 2.2.10 on 2021-12-08 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elastics', '0005_auto_20211208_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breakerconfig',
            name='fielddata_over',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Fielddata overhead'),
        ),
        migrations.AlterField(
            model_name='breakerconfig',
            name='inflight_req',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Inflight_requests overhead'),
        ),
    ]
