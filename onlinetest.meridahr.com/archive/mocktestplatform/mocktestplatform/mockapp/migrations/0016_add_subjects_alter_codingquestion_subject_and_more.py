# Generated by Django 5.0.1 on 2024-02-05 11:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mockapp', '0015_alter_student_result_coding_marks_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='add_subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default=' ', max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='codingquestion',
            name='subject',
            field=models.CharField(choices=[('python', 'Python'), ('java', 'Java'), ('javascript', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS'), ('bootstrap', 'Bootstrap')], default=' ', max_length=200),
        ),
        migrations.AlterField(
            model_name='codingquestion',
            name='test_level',
            field=models.CharField(choices=[('basic', 'Basic'), ('intermediate', 'Intermediate'), ('advance', 'Advance')], default='testlevel', max_length=200),
        ),
        migrations.AlterField(
            model_name='student_result',
            name='coding_marks',
            field=models.CharField(default='....', max_length=100),
        ),
        migrations.CreateModel(
            name='Coding_Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_level', models.CharField(choices=[('basic', 'Basic'), ('intermediate', 'Intermediate'), ('advance', 'Advance')], default='testlevel', max_length=200)),
                ('question_text', models.TextField(default='question_text')),
                ('code_snippet', models.TextField(default='code_snipet')),
                ('correct_answer', models.TextField(default='correct_answer')),
                ('subject', models.ForeignKey(default=' ', max_length=200, on_delete=django.db.models.deletion.CASCADE, to='mockapp.add_subjects')),
            ],
        ),
    ]
