# Generated by Django 4.2.11 on 2024-04-08 08:38

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("term", "0007_alter_term_name"),
        ("accounts", "0013_alter_student_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="average",
            field=models.FloatField(blank=True, null=True, verbose_name="معدل کل"),
        ),
        migrations.CreateModel(
            name="StudentTermAverage",
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
                    "average",
                    models.FloatField(blank=True, null=True, verbose_name="معدل ترم"),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_term_average_student",
                        to="accounts.student",
                        verbose_name="دانشجو",
                    ),
                ),
                (
                    "term",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student_term_average_term",
                        to="term.term",
                        verbose_name="ترم",
                    ),
                ),
            ],
        ),
    ]
