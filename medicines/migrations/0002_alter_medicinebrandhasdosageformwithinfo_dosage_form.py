# Generated by Django 4.1.12 on 2023-10-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("medicines", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicinebrandhasdosageformwithinfo",
            name="dosage_form",
            field=models.CharField(
                choices=[
                    ("T", "Tablet"),
                    ("S", "Capsule"),
                    ("O", "Ointment"),
                    ("I", "Injection"),
                ],
                max_length=128,
                verbose_name="medicine brand dosage form",
            ),
        ),
    ]
