# Generated by Django 4.1.2 on 2023-03-24 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0007_mainskill_norm_delete_skillnorm'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='weight',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]