# Generated by Django 4.1.2 on 2023-04-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0012_rename_employee_userskill_employee_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='period',
            name='period_position',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
