# Generated by Django 4.1.1 on 2022-09-10 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_student_grade_alter_incident_referral_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='referral_url',
            field=models.URLField(),
        ),
    ]
