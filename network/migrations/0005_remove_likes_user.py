# Generated by Django 3.1.1 on 2020-10-31 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20201031_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likes',
            name='user',
        ),
    ]
