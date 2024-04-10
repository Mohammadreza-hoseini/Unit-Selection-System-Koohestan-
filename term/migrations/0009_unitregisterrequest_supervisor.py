# Generated by Django 4.2.11 on 2024-04-09 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0016_alter_studenttermaverage_student_and_more"),
        ("term", "0008_unitregisterrequest_term"),
    ]

    operations = [
        migrations.AddField(
            model_name="unitregisterrequest",
            name="supervisor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="unit_register_request_supervisor",
                to="accounts.professor",
                verbose_name="استاد راهنما",
            ),
        ),
    ]