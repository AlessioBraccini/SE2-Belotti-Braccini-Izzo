# Generated by Django 4.0 on 2022-01-06 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_delete_helprequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farm',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
