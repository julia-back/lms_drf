# Generated by Django 5.1.8 on 2025-04-05 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0007_remove_lesson_updated_at_alter_course_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
