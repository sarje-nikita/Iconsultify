# Generated by Django 4.2 on 2023-04-24 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0006_countrytable_beer_in_a_pub_countrytable_cappuccino_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrytable',
            name='Cheap_bedroom_apartment',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='House_price_to_Buy_in_Suburbs',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Internet_plan',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Local_transport_ticket',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Mortgage_Interest_Rate_for_Years',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Taxi_Ride',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Utility_Bill_for_a_Family',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Utility_Bill_one_person',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='_Apartment_price_to_Buy_in_city_Center',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='_Monthly_ticket_local_transport',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='_bedroom_apartment_in_city_Center',
            field=models.FloatField(default=0),
        ),
    ]
