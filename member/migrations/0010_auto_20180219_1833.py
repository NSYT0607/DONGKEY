# Generated by Django 2.0.1 on 2018-02-19 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_auto_20180213_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='absence',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='member',
        ),
        migrations.DeleteModel(
            name='Absence',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]
