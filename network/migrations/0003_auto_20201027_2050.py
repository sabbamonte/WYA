# Generated by Django 3.1.1 on 2020-10-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_new_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='new_post',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
