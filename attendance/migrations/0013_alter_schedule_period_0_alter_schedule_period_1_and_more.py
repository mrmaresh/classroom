# Generated by Django 4.0.4 on 2022-05-30 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_schedule_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='period_0',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_1',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_2',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_3',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_4',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_5',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_6',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_7',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='period_8',
            field=models.CharField(max_length=20),
        ),
    ]