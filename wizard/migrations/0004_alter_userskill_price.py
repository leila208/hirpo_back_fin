# Generated by Django 4.2 on 2023-04-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0003_evaluation_frequency_freq_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userskill',
            name='price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
