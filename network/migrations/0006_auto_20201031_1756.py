# Generated by Django 3.1.1 on 2020-10-31 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_likes_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likes',
            old_name='post',
            new_name='like_id',
        ),
    ]
