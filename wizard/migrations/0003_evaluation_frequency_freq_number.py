# Generated by Django 4.2 on 2023-04-19 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0002_alter_departmentposition_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation_frequency',
            name='freq_number',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
