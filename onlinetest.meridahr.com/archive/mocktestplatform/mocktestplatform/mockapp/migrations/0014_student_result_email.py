# Generated by Django 5.0 on 2024-01-10 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockapp', '0013_student_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_result',
            name='email',
            field=models.EmailField(default='Not Exist', max_length=254),
        ),
    ]
