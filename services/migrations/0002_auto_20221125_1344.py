# Generated by Django 3.2.9 on 2022-11-25 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='amount',
            new_name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='userrecord',
            name='parking_slot_details',
        ),
        migrations.AddField(
            model_name='userrecord',
            name='amount_paid',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='userrecord',
            name='parking_slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.appointment'),
        ),
    ]