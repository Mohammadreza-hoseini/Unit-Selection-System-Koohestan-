# Generated by Django 4.2.11 on 2024-03-26 16:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_professor_past_teaching_lessons_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OTPCode",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("code", models.CharField(max_length=6, verbose_name="کد یکبار مصرف")),
                ("email", models.EmailField(max_length=254, verbose_name="ایمیل")),
            ],
        ),
    ]
