# Generated by Django 4.1.2 on 2023-02-26 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0003_remove_departmentskillnorm_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdepartment',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wizard.project'),
        ),
    ]
