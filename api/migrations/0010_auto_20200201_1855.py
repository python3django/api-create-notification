# Generated by Django 3.0.2 on 2020-02-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200201_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='username',
            field=models.CharField(blank=True, max_length=300, verbose_name='Имя'),
        ),
    ]
