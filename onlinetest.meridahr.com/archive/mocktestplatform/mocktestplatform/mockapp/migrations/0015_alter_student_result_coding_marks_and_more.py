# Generated by Django 5.0 on 2024-01-11 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockapp', '0014_student_result_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_result',
            name='coding_marks',
            field=models.TextField(default='....', max_length=100),
        ),
        migrations.AlterField(
            model_name='student_result',
            name='contact_number',
            field=models.CharField(default='not entered', max_length=250),
        ),
        migrations.AlterField(
            model_name='student_result',
            name='mcq_marks',
            field=models.CharField(default='....', max_length=100),
        ),
        migrations.AlterField(
            model_name='student_result',
            name='student_id',
            field=models.CharField(default='....', max_length=10),
        ),
        migrations.AlterField(
            model_name='student_result',
            name='student_name',
            field=models.CharField(default='Not entered', max_length=200),
        ),
        migrations.AlterField(
            model_name='student_result',
            name='test_taken',
            field=models.CharField(default='.....', max_length=200),
        ),
    ]
