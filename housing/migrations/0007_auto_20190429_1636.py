# Generated by Django 2.1.5 on 2019-04-29 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0006_auto_20190429_1628'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='max_price',
        ),
        migrations.RemoveField(
            model_name='building',
            name='min_price',
        ),
    ]
