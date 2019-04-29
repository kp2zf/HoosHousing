# Generated by Django 2.1.5 on 2019-04-29 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing', '0007_auto_20190429_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='max_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='min_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
