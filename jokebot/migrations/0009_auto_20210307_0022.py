# Generated by Django 3.1.7 on 2021-03-07 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jokebot', '0008_auto_20210306_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jokebotai',
            name='heard_knock_knock',
        ),
        migrations.RemoveField(
            model_name='jokebotai',
            name='heard_setup',
        ),
        migrations.AddField(
            model_name='jokebotai',
            name='knock_knock',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='jokebotai',
            name='setup',
            field=models.BooleanField(default=False),
        ),
    ]
