# Generated by Django 4.2.11 on 2024-03-28 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_otpcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="military_service_status",
            field=models.PositiveSmallIntegerField(
                choices=[
                    (1, "permanentExemption"),
                    (2, "educationPardon"),
                    (3, "inductee"),
                ],
                verbose_name="وضعیت نظام وظیفه",
            ),
        ),
        migrations.AlterField(
            model_name="university",
            name="educational_assistant",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="university_educational_assistant",
                to="accounts.professor",
                verbose_name="معاون آموزشی دانشگاه",
            ),
        ),
        migrations.AlterField(
            model_name="university",
            name="university_president",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="university_university_president",
                to="accounts.professor",
                verbose_name="رئیس دانشگاه",
            ),
        ),
    ]
