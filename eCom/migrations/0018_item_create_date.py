# Generated by Django 3.2.4 on 2021-06-19 03:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('eCom', '0017_auto_20210618_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 19, 3, 32, 39, 254054, tzinfo=utc)),
        ),
    ]
