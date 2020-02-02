from ckeditor_uploader.fields import RichTextUploadingField
from django.core.exceptions import ValidationError
from django.db import models


class Template(models.Model):
    '''
    Шаблон уведомления
    '''

    TEMPLATE_CHOICES = (
        ('client_registration_email', 'Подтверждение электронной почты при регистрации'),
        ('client_registration_sms', 'Подтверждение телефона при регистрации'),
        ('client_forgot_password_email', 'Восстановление забытого пароля по электронной почте'),
        ('client_forgot_password_sms', 'Восстановление пароля по телефону'),
        ('client_invoice_email', 'Сформирован новый счет'),
    )

    title = models.CharField(
        verbose_name='Шаблон уведомления',
        unique=True,
        choices=TEMPLATE_CHOICES,
        max_length=100,
    )

    content = RichTextUploadingField(
        verbose_name='Контент',
    )

    is_notification_sms = models.BooleanField(
        verbose_name='Уведомления по SMS',
        default=False,
    )

    is_notification_email = models.BooleanField(
        verbose_name='Уведомления по Электронной почте',
        default=False,
    )

    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'шаблон'
        verbose_name_plural = 'шаблоны'

    def __str__(self):
        return self.title


class Notification(models.Model):
    '''
    Уведомление
    '''

    template = models.ForeignKey(
        verbose_name='Шаблон',
        to=Template,
        on_delete=models.SET_NULL,
        related_name='notifications',
        blank=True,
        null=True,
    )

    username = models.CharField(
        verbose_name='Имя',
        max_length=300,
        blank=True,
    )

    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=200,
        blank=True,
    )

    phone = models.CharField(
        verbose_name='Телефон',
        max_length=50,
        blank=True,
    )

    link = models.URLField(
        verbose_name='Ссылка',
        max_length=250,
        blank=True,
    )

    invoice_id = models.CharField(
        verbose_name='Id Счёта',
        max_length=50,
        blank=True,
    )

    invoice_number = models.CharField(
        verbose_name='Номер Счёта',
        max_length=50,
        blank=True,
    )

    invoice_date = models.CharField(
        verbose_name='Дата формирования счёта',
        max_length=50,
        blank=True
    )

    reporting_period = models.CharField(
        verbose_name='Отчётный период',
        max_length=100,
        blank=True
    )

    message_id = models.CharField(
        verbose_name='Id Сообщения',
        max_length=50,
        blank=True,
    )

    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def clean(self):
        if not self.email and not self.phone:
            raise ValidationError(
                'Необходимо заполнить либо поле «Электронная почта» либо поле «Телефон»')

    def __str__(self):
        notification_list = [str(self.created), str(self.template)]
        if self.email:
            notification_list.append(self.email)
        if self.phone:
            notification_list.append(self.phone)
        return ' - '.join(notification_list)


class Preference(models.Model):
    """
    Настройки
    """

    email = models.EmailField(
        verbose_name='Электронная почта отправителя',
        max_length=200,
    )

    phone = models.CharField(
        verbose_name='Телефон отправителя',
        max_length=50,
    )

    test_email = models.EmailField(
        verbose_name='Тестовая электронная почта получателя',
        max_length=200,
    )

    test_phone = models.CharField(
        verbose_name='Тестовый телефон получателя',
        max_length=50,
    )

    class Meta:
        verbose_name = 'настройки'
        verbose_name_plural = 'настройки'

    def __str__(self):
        return 'Настройки'
