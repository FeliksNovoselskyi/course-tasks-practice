# Generated by Django 4.2.7 on 2024-08-19 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0006_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_index', models.PositiveIntegerField(default=0)),
                ('completed_sentences', models.ManyToManyField(blank=True, related_name='completed_by_users', to='course.taskdata')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]