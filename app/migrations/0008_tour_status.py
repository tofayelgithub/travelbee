# Generated by Django 4.1.2 on 2023-06-21 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_tour_total_seats_alter_booking_tour'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='status',
            field=models.CharField(choices=[('announced', 'Announced'), ('booking', 'Booking'), ('running', 'Running'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='announced', max_length=20),
        ),
    ]
