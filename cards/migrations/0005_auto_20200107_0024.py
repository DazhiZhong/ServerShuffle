# Generated by Django 3.0.1 on 2020-01-07 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_currentdeck_userhashtag'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userhashtag',
            old_name='card',
            new_name='user',
        ),
    ]