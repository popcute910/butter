# Generated by Django 3.2.14 on 2022-07-31 09:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('butter', '0005_rename_instapost_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(default=1, max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.RegexValidator('^[a-zA-Z0-9]*$')], verbose_name='Username'),
        ),
    ]