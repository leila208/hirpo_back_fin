# Generated by Django 4.1.2 on 2023-03-18 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wizard', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Skill',
            new_name='MainSkill',
        ),
        migrations.AlterModelOptions(
            name='departmentposition',
            options={'verbose_name': 'Position', 'verbose_name_plural': 'Positions'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='projectdepartment',
            options={'verbose_name': 'Department', 'verbose_name_plural': 'Departments'},
        ),
        migrations.AlterModelOptions(
            name='skillnorm',
            options={'ordering': ['position__department__name', 'position__name', 'skill__name'], 'verbose_name': 'Comptency norm', 'verbose_name_plural': 'Comptency norms'},
        ),
    ]