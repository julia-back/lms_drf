# Generated by Django 5.1.6 on 2025-03-06 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_payment_payment_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="payment_link",
            field=models.URLField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]
