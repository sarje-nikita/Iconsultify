# Generated by Django 4.2 on 2023-05-23 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrape', '0013_statetable_citytable_state_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='citytable',
            name='Liveability',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='countrytable',
            name='Quality_of_life',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='statetable',
            name='Quality_of_life',
            field=models.FloatField(default=0),
        ),
    ]
