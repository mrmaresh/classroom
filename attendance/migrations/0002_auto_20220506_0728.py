# Generated by Django 3.0.14 on 2022-05-06 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='student_id',
        ),
        migrations.AddField(
            model_name='record',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student', to='attendance.Student'),
            preserve_default=False,
        ),
    ]
