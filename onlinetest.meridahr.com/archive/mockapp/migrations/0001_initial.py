# Generated by Django 5.0 on 2023-12-12 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mcq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('optionA', models.CharField(max_length=500)),
                ('optionB', models.CharField(max_length=500)),
                ('optionC', models.CharField(max_length=500)),
                ('optionD', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
            ],
        ),
    ]
