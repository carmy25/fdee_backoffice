# Generated by Django 5.1 on 2025-01-19 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0011_receipt_payment_metnod"),
    ]

    operations = [
        migrations.RenameField(
            model_name="receipt",
            old_name="payment_metnod",
            new_name="payment_method",
        ),
    ]
