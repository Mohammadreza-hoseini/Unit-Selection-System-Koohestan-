# Generated by Django 4.2.11 on 2024-04-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0004_alter_course_term"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subject",
            name="mandatory",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "yes"), (2, "no")],
                default=1,
                verbose_name="وضعیت اجباری بودن یا نبودن درس",
            ),
        ),
    ]
