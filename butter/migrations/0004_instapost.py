# Generated by Django 3.2.14 on 2022-07-30 07:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('butter', '0003_auto_20220725_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instapost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_text', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
                ('post_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
