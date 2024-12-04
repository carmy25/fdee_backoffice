# Generated by Django 5.1 on 2024-11-30 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0004_remove_receipt_created_receipt_created_at_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productitem",
            name="product",
        ),
        migrations.AddField(
            model_name="productitem",
            name="amount",
            field=models.PositiveSmallIntegerField(default=0, verbose_name="кількість"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="productitem",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=6, verbose_name="ціна"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="productitem",
            name="product_type",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_items",
                to="order.product",
                verbose_name="продукт",
            ),
            preserve_default=False,
        ),
    ]
