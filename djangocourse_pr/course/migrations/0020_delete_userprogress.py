# Generated by Django 4.2.7 on 2024-08-30 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProgress',
        ),
    ]
