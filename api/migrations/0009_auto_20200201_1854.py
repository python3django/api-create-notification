# Generated by Django 3.0.2 on 2020-02-01 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200201_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='template',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications', to='api.Template', verbose_name='Шаблон'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='username',
            field=models.CharField(max_length=300, verbose_name='Имя'),
        ),
    ]