# Generated by Django 5.2.1 on 2025-06-16 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=150)),
                ('location', models.CharField(blank=True, max_length=150)),
                ('description', models.TextField()),
                ('posted_date', models.DateField(auto_now_add=True)),
                ('application_link', models.URLField(blank=True)),
            ],
        ),
    ]
