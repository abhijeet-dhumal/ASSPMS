# Generated by Django 3.2.9 on 2022-11-27 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20221127_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentslot',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='appointmentslot',
            name='start_time',
            field=models.TimeField(),
        ),
    ]