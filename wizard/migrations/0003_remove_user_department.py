# Generated by Django 4.1.2 on 2023-03-23 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0002_remove_mainskill_department_mainskill_position_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='department',
        ),
    ]