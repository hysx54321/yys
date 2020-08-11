# Generated by Django 3.0.2 on 2020-08-10 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BasicModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('time_created', models.PositiveIntegerField()),
                ('time_modified', models.PositiveIntegerField()),
                ('deleted', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='income_calculator.BasicModel')),
                ('display_name', models.CharField(max_length=200)),
                ('min', models.IntegerField()),
                ('max', models.IntegerField()),
                ('expectation_value', models.IntegerField()),
                ('default_frequency', models.IntegerField()),
                ('default_total', models.IntegerField()),
                ('priority', models.SmallIntegerField()),
                ('period_id', models.PositiveIntegerField()),
                ('item_id', models.PositiveIntegerField()),
                ('icon', models.TextField()),
            ],
            bases=('income_calculator.basicmodel',),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='income_calculator.BasicModel')),
            ],
            bases=('income_calculator.basicmodel',),
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('basicmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='income_calculator.BasicModel')),
                ('num_days', models.PositiveIntegerField()),
            ],
            bases=('income_calculator.basicmodel',),
        ),
    ]