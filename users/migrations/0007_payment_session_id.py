# Generated by Django 5.1.6 on 2025-03-06 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_payment_payment_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="session_id",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
