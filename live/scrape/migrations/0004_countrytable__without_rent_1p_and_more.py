# Generated by Django 4.2 on 2023-04-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0003_countrytable_total_with_rent_3p'),
    ]

    operations = [
        migrations.AddField(
            model_name='countrytable',
            name='_Without_rent_1p',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='_Without_rent_3p',
            field=models.FloatField(default=0),
        ),
    ]