# Generated by Django 5.1 on 2025-02-12 13:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0012_rename_payment_metnod_receipt_payment_method"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productitem",
            name="price",
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="products",
                to="order.category",
                verbose_name="категорія",
            ),
        ),
    ]
