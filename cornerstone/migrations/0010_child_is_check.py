# Generated by Django 2.0.6 on 2018-08-28 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cornerstone', '0009_auto_20180826_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='is_check',
            field=models.BooleanField(default=False),
        ),
    ]
