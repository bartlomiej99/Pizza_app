# Generated by Django 4.0.1 on 2022-01-23 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza_elk', '0014_alter_billingaddress_additional_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='additional_information',
            field=models.CharField(max_length=128),
        ),
    ]
