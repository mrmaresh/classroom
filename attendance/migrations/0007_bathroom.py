# Generated by Django 4.0.4 on 2022-05-24 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_student_exception'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bathroom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time_out', models.DateTimeField()),
                ('time_back', models.DateTimeField()),
                ('minutes', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_bathroom', to='attendance.student')),
            ],
        ),
    ]
