# Generated by Django 2.1.15 on 2020-08-03 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapi', '0023_ticketdetails_ticket_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketdetails',
            name='ticket_picture',
            field=models.ImageField(blank=True, max_length=300, null=True, upload_to=''),
        ),
    ]
