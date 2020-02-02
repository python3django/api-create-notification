# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os

from django.contrib import admin, messages
from django.template import Context, Template
from django_object_actions import DjangoObjectActions
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from singlemodeladmin import SingleModelAdmin

from . import models


@admin.register(models.Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_notification_sms',
        'is_notification_email',
        'created'
    ]
    search_fields = ['title']
    list_filter = ['title']


@admin.register(models.Notification)
class NotificationAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = [
        'template',
        'username',
        'email',
        'phone',
        'created'
    ]
    search_fields = [
        'email',
        'phone'
    ]
    list_filter = ['template']

    def notification_email(self, request, obj):
        letter = models.Template.objects.get(pk=obj.template.pk)
        content = Template(letter.content).render(
            Context({
                'username': obj.username,
                'email': obj.email,
                'link': obj.link,
                'invoice_id': obj.invoice_id,
                'invoice_number': obj.invoice_number,
                'invoice_date': obj.invoice_date,
                'reporting_period': obj.reporting_period,
            })
        )
        preference = models.Preference.objects.first() or {}
        subject=[x[1] for x in models.Template.TEMPLATE_CHOICES if x[0] == obj.template.title]
        message = Mail(
            from_email=preference.email,
            to_emails=obj.email,
            subject=subject[0],
            html_content=content
        )
        print(message)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            messages.add_message(
                request,
                messages.SUCCESS,
                'Письмо успешно отправлено')
        except Exception as e:
            print(e.message)
            messages.add_message(
                request,
                messages.ERROR,
                'Ошибка! Письмо не отправлено')
    notification_email.label = 'Email уведомление' # yapf: disable
    notification_email.short_description = 'Отправить Email уведомление'

    def notification_sms(self, request, obj):
        letter = models.Template.objects.get(pk=obj.template)
        content = Template(letter.content).render(
            Context({
                'username': obj.username,
                'phone': obj.phone,
            }))
        # TODO
    notification_sms.label = 'SMS уведомление' # yapf: disable
    notification_sms.short_description = 'Отправить SMS уведомление'

    change_actions = ['notification_email', 'notification_sms']


@admin.register(models.Preference)
class PreferenceAdmin(SingleModelAdmin):
    pass
