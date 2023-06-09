# Generated by Django 4.2 on 2023-06-08 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_purchase", "0012_transaction_tickets_transaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tickets",
            name="timestamp",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="transaction",
            name="qr_code",
            field=models.ImageField(upload_to="transaction_qr/"),
        ),
    ]