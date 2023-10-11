# Generated by Django 4.1.12 on 2023-10-11 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_useraccount_blood_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, help_text='Required. 128 characters or fewer.', max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
