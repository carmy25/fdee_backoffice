# Generated by Django 5.1 on 2025-01-18 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0008_alter_receipt_updated_at"),
        ("place", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="receipt",
            name="place",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="place.place",
                verbose_name="місце",
            ),
        ),
    ]
