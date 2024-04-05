# Generated by Django 4.2.11 on 2024-04-03 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0005_alter_subject_mandatory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="course_type",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "basic"),
                    (2, "specialized"),
                    (3, "general"),
                    (4, "practical"),
                ],
                default=1,
                verbose_name="نوع درس",
            ),
        ),
    ]
