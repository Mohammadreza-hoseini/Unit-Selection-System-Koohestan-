# Generated by Django 4.2.11 on 2024-04-11 08:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0016_alter_studenttermaverage_student_and_more"),
        ("course", "0006_alter_subject_course_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScoreTable",
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
                ("score", models.IntegerField(default=-1, verbose_name="نمره")),
                (
                    "course_pass_status",
                    models.IntegerField(
                        choices=[(1, "passed"), (-1, "failed"), (0, "pending")],
                        default=0,
                        verbose_name="وضعیت قبولی درس ترمی",
                    ),
                ),
                ("score_finalized_status", models.BooleanField(default=False)),
                (
                    "reconsideration_status",
                    models.IntegerField(
                        choices=[
                            (0, "no appeal request"),
                            (-1, "rejected"),
                            (1, "accepted"),
                            (2, "pending"),
                        ],
                        default=0,
                        verbose_name="وضعیت درخواست تجدید نظر",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="score_course",
                        to="course.course",
                        verbose_name="درس ترمی",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_score",
                        to="accounts.student",
                        verbose_name="دانشجو",
                    ),
                ),
            ],
        ),
    ]
