# Generated by Django 2.1.15 on 2020-07-12 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrationapi', '0002_auto_20200712_2350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='uname',
        ),
    ]
