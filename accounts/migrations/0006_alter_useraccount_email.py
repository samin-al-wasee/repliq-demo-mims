# Generated by Django 4.1.12 on 2023-10-13 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_useraccount_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email already exists.'}, help_text='Required. 128 characters or fewer.', max_length=254, unique=True, verbose_name='email address'),
        ),
    ]
