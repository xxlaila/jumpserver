# Generated by Django 2.2.10 on 2021-11-06 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0050_assetexpansion_balanced_diskinfo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='balanced',
            options={'ordering': ['ip'], 'verbose_name': 'Balanced'},
        ),
    ]