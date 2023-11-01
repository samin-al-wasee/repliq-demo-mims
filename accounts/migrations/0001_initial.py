# Generated by Django 4.1.12 on 2023-11-01 03:28

import uuid

import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import accounts.managers
import accounts.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "email",
                    models.EmailField(
                        error_messages={"unique": "Email already exists."},
                        help_text="Required. Unique. 128 characters or fewer.",
                        max_length=254,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={"unique": "Username already exists."},
                        help_text="Required. Unique. 128 characters or fewer.",
                        max_length=128,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.ASCIIUsernameValidator(),
                            django.core.validators.MinLengthValidator(limit_value=8),
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True,
                        help_text="Optional. 128 characters or fewer.",
                        max_length=128,
                        verbose_name="first_name",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True,
                        help_text="Optional. 128 characters or fewer.",
                        max_length=128,
                        verbose_name="last_name",
                    ),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True,
                        help_text="Optional. YYYY-MM-DD format.",
                        null=True,
                        verbose_name="date of birth",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=accounts.models.User._rename_photo,
                        verbose_name="user photo",
                    ),
                ),
                (
                    "height_cm",
                    models.IntegerField(
                        default=-1,
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=1)
                        ],
                        verbose_name="height in centimetres",
                    ),
                ),
                (
                    "weight_kg",
                    models.IntegerField(
                        default=-1,
                        validators=[
                            django.core.validators.MinValueValidator(limit_value=1)
                        ],
                        verbose_name="weight in kilograms",
                    ),
                ),
                (
                    "blood_group",
                    models.CharField(
                        choices=[
                            ("a+", "A Positive"),
                            ("a-", "A Negative"),
                            ("b+", "B Positive"),
                            ("b-", "B Negative"),
                            ("ab+", "AB Positive"),
                            ("ab-", "AB Negative"),
                            ("o+", "O Positive"),
                            ("o-", "O Negative"),
                            ("unknown", "Unknown"),
                        ],
                        default="unknown",
                        max_length=128,
                        verbose_name="blood group",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("male", "Male"),
                            ("female", "Female"),
                            ("other", "Other"),
                            ("unknown", "Unknown"),
                        ],
                        default="unknown",
                        max_length=128,
                        verbose_name="gender",
                    ),
                ),
                (
                    "address",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="common.address",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
            managers=[
                ("objects", accounts.managers.UserManager_()),
            ],
        ),
    ]
