# Generated by Django 2.1.15 on 2020-07-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interestsapi', '0002_auto_20200709_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinterests',
            name='ticket_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='allinterests',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
