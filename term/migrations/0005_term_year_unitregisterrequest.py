# Generated by Django 4.2.11 on 2024-04-05 17:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0006_alter_subject_course_type"),
        ("accounts", "0012_alter_student_lessons_in_progress_and_more"),
        ("term", "0004_remove_term_course_lists_remove_term_professors_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="term",
            name="year",
            field=models.DateField(
                auto_now_add=True, default="2024-05-18", verbose_name="سال جاری"
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="UnitRegisterRequest",
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
                (
                    "request_state",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "pending"), (2, "accepted"), (3, "rejected")],
                        default=1,
                        verbose_name="وضعیت درخواست",
                    ),
                ),
                (
                    "course",
                    models.ManyToManyField(
                        related_name="unit_register_request_course",
                        to="course.course",
                        verbose_name="دروس",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="unit_register_request_student",
                        to="accounts.student",
                        verbose_name="دانشجو",
                    ),
                ),
            ],
        ),
    ]
