# Generated by Django 2.0.6 on 2018-10-26 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cornerstone', '0012_auto_20181026_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='driver_user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='cornerstone.StaffUser'),
            preserve_default=False,
        ),
    ]
