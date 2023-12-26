# Generated by Django 3.2.9 on 2022-11-27 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20221125_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrecord',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='entry_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userrecord',
            name='exit_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
