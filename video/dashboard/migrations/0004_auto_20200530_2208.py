# Generated by Django 3.0.6 on 2020-05-30 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_remove_clientuser_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientuser',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='clientuser',
            name='gender',
        ),
    ]
