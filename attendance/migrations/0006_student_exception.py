# Generated by Django 4.0.4 on 2022-05-23 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_alter_record_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='exception',
            field=models.BinaryField(default=False),
            preserve_default=False,
        ),
    ]
