# Generated by Django 4.2.16 on 2024-09-24 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='voted',
            field=models.BooleanField(default=False),
        ),
    ]
