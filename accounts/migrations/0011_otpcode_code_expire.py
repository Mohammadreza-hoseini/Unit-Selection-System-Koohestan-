# Generated by Django 4.2.11 on 2024-04-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0010_professor_term_student_term"),
    ]

    operations = [
        migrations.AddField(
            model_name="otpcode",
            name="code_expire",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="زمان منقضی شدن کد یکبار مصرف"
            ),
        ),
    ]
