# Generated by Django 5.1 on 2024-11-14 12:34

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0003_alter_product_options_alter_receipt_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="receipt",
            name="created",
        ),
        migrations.AddField(
            model_name="receipt",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="дата створення",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="receipt",
            name="number",
            field=models.PositiveIntegerField(
                default=True, null=True, verbose_name="номер"
            ),
        ),
    ]
