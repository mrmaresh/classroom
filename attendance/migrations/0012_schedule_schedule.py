# Generated by Django 4.0.4 on 2022-05-27 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_alter_schedule_period_0_alter_schedule_period_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='schedule',
            field=models.CharField(default='regular', max_length=20),
            preserve_default=False,
        ),
    ]
