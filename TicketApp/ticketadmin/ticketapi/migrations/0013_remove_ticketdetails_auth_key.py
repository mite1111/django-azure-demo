# Generated by Django 2.1.15 on 2020-07-09 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapi', '0012_ticketdetails_ticketdescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketdetails',
            name='Auth_Key',
        ),
    ]
