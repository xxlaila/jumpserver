# Generated by Django 2.2.13 on 2020-11-10 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminal', '0027_auto_20201102_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terminal',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Name'),
        ),
    ]
