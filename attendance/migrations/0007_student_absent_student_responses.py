# Generated by Django 4.1 on 2022-08-21 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0006_incident'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='absent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='responses',
            field=models.IntegerField(default=0),
        ),
    ]
