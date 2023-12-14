# Generated by Django 4.2 on 2023-04-24 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0005_countrytable_rent_and_utilities_1p_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrytable',
            name='Beer_in_a_Pub',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Cappuccino',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Dinner_in_a_Restaurant',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Fast_food_meal',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Lunch_Menu',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Monthly_salary_after_tax',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Pepsi_Coke',
            field=models.FloatField(default=0),
        ),
    ]
