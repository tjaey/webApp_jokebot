# Generated by Django 3.1.7 on 2021-03-06 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jokebot', '0006_auto_20210306_2330'),
    ]

    operations = [
        migrations.AddField(
            model_name='jokebotai',
            name='heard_setup',
            field=models.BooleanField(default=False),
        ),
    ]
