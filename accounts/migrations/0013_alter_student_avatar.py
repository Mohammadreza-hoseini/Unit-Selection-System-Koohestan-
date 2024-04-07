# Generated by Django 4.2.11 on 2024-04-07 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0012_alter_student_lessons_in_progress_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="avatars/",
                verbose_name="تصویر پروفایل",
            ),
        ),
    ]