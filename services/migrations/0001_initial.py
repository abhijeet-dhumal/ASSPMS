# Generated by Django 3.2.9 on 2022-10-15 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_accepted', models.BooleanField(default=None, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('vehicle_image', models.ImageField(upload_to='')),
                ('license_plate', models.ImageField(upload_to='')),
                ('license_plate_text', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('text', models.TextField(max_length=500)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('is_accepted', models.BooleanField(default=None)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.appointment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AppointmentSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateField()),
                ('is_available', models.BooleanField(default=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('slot_details', models.TextField(blank=True, max_length=500, null=True)),
                ('is_verified', models.BooleanField(default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.appointmentslot'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
