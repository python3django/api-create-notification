# Generated by Django 3.0.2 on 2020-02-01 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_notification_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='invoice_date',
            field=models.CharField(blank=True, max_length=50, verbose_name='Дата формирования счёта'),
        ),
        migrations.AddField(
            model_name='notification',
            name='invoice_id',
            field=models.CharField(blank=True, max_length=50, verbose_name='Id Счёта'),
        ),
        migrations.AddField(
            model_name='notification',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=50, verbose_name='Номер Счёта'),
        ),
        migrations.AddField(
            model_name='notification',
            name='reporting_period',
            field=models.CharField(blank=True, max_length=100, verbose_name='Отчётный период'),
        ),
        migrations.AlterField(
            model_name='template',
            name='title',
            field=models.CharField(choices=[('client_register_email', 'Подтверждение электронной почты при регистрации'), ('client_register_sms', 'Подтверждение телефона при регистрации'), ('client_forgot_password_email', 'Восстановление забытого пароля по электронной почте'), ('client_forgot_password_sms', 'Восстановление пароля по телефону'), ('client_invoice_email', 'Сформирован новый счет')], max_length=100, unique=True, verbose_name='Шаблон уведомления'),
        ),
    ]