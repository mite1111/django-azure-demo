# Generated by Django 2.1.15 on 2020-06-30 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapi', '0004_auto_20200630_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketdetails',
            name='TicketId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
