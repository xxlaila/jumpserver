# Generated by Django 2.2.10 on 2021-12-08 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elastics', '0006_auto_20211208_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routingconfignum',
            name='routingConfig',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elastics.RoutingConfig', verbose_name='RoutingConfig'),
        ),
    ]
