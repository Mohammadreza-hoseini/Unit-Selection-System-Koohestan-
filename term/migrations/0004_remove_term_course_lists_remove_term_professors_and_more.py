# Generated by Django 4.2.11 on 2024-04-02 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("term", "0003_alter_term_students"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="term",
            name="course_lists",
        ),
        migrations.RemoveField(
            model_name="term",
            name="professors",
        ),
        migrations.RemoveField(
            model_name="term",
            name="students",
        ),
    ]
