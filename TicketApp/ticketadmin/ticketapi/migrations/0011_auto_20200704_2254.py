# Generated by Django 2.1.15 on 2020-07-04 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapi', '0010_auto_20200704_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketdetails',
            name='Product',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
