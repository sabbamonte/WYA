# Generated by Django 3.1.4 on 2020-12-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20201216_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='avatar',
            field=models.ImageField(upload_to='images'),
        ),
    ]
