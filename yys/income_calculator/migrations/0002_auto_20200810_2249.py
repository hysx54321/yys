# Generated by Django 3.1 on 2020-08-10 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('income_calculator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicmodel',
            name='description',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='event',
            name='display_name',
            field=models.CharField(max_length=20),
        ),
    ]
