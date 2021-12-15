# Generated by Django 4.0 on 2021-12-14 01:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query_Archived',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query_string', models.TextField(max_length=10000)),
                ('query_name', models.TextField(max_length=200, null=True)),
                ('geo', models.BooleanField(default=0)),
                ('date_created_at', models.DateField(default=datetime.date(2021, 12, 14))),
            ],
        ),
    ]