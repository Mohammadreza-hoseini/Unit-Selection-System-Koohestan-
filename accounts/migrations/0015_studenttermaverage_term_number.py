# Generated by Django 4.2.11 on 2024-04-08 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0014_alter_student_average_studenttermaverage"),
    ]

    operations = [
        migrations.AddField(
            model_name="studenttermaverage",
            name="term_number",
            field=models.PositiveIntegerField(default=1, verbose_name="شماره ترم"),
        ),
    ]
