# Generated by Django 4.2.9 on 2024-01-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_fan_education_alter_fan_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bandmember',
            name='gender',
            field=models.CharField(choices=[('男', '男'), ('女', '女')], max_length=10, verbose_name='性别'),
        ),
    ]
