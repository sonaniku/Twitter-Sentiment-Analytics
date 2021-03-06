# Generated by Django 4.0 on 2021-12-13 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_id', models.CharField(max_length=50, unique=True)),
                ('oauth_token', models.CharField(max_length=150)),
                ('oauth_secret', models.CharField(max_length=150)),
                ('user_id', models.CharField(max_length=100)),
                ('user_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Query_Archived',
        ),
    ]
