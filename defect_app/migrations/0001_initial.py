# Generated by Django 5.1.3 on 2024-11-27 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefectDetection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100)),
                ('model_type', models.CharField(max_length=20)),
                ('inspection_date', models.DateTimeField(auto_now_add=True)),
                ('defect_results', models.JSONField()),
                ('image', models.ImageField(upload_to='defect_images/')),
            ],
            options={
                'ordering': ['-inspection_date'],
            },
        ),
    ]
