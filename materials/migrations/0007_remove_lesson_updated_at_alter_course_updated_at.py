# Generated by Django 5.1.6 on 2025-03-12 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0006_lesson_updated_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lesson",
            name="updated_at",
        ),
        migrations.AlterField(
            model_name="course",
            name="updated_at",
            field=models.DateTimeField(),
        ),
    ]
