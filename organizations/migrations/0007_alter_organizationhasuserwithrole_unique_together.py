# Generated by Django 4.1.12 on 2023-10-16 06:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("organizations", "0006_organizationhasuserwithrole"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="organizationhasuserwithrole",
            unique_together={("organization", "user_account")},
        ),
    ]
