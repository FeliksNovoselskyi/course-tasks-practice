# Generated by Django 4.2.7 on 2024-08-15 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0005_remove_taskdata_task_delete_task_delete_taskdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('lesson_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='course.lesson')),
                ('name', models.CharField(max_length=10)),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='excel_files/')),
                ('additional_words_file', models.FileField(blank=True, null=True, upload_to='additional_words_files/')),
            ],
            bases=('course.lesson',),
        ),
        migrations.CreateModel(
            name='TaskData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column1', models.CharField(max_length=255)),
                ('column2', models.CharField(max_length=255)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_data', to='course.task')),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_words', to='course.task')),
            ],
        ),
    ]
