# Generated by Django 3.0.6 on 2020-05-30 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20200528_1008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientuser',
            name='birthday',
        ),
    ]
