# Generated by Django 4.2.11 on 2024-03-31 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_remove_educationalassistant_assistant_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="educationalassistant",
            old_name="professor",
            new_name="assistant",
        ),
    ]
