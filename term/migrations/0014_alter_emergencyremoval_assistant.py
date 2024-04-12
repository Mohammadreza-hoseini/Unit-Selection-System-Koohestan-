# Generated by Django 4.2.11 on 2024-04-12 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_studenttermaverage_student_and_more'),
        ('term', '0013_alter_emergencyremoval_assistant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencyremoval',
            name='assistant',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='emergency_removal_assistant', to='accounts.educationalassistant', verbose_name='معاون آموزشی'),
            preserve_default=False,
        ),
    ]
