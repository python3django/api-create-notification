# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python

import json
import logging
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, Template
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from . import models, serializers

logger = logging.getLogger('api')


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def notification_create(request):
    # Пример запросов программой httpie:
    # http POST 127.0.0.1:8000/api/v1/notification/ template="client_registration_email" \
    # content:='{"username": "Man5", "email": "django2shop@gmail.com", \
    # "link": "http://site.com/registration/abcdfegkl/"}'

    # http POST 127.0.0.1:8000api/v1/notification/ template="client_invoice_email" \
    # content:='{"username": "Man5", "email": "django2shop@gmail.com", \
    # "link": "http://site.com/invoice/abcdfegkl/", "invoice_id": "afdadf6546", \
    # "invoice_number": "5", "invoice_date": "01 февраля 2020", \
    # "reporting_period": "c 01 января 2020 по 31 января 2020"}'

    if request.method == 'POST':
        notification_data = JSONParser().parse(request)
        template_data = notification_data.get('template', '')
        content_data = notification_data.get('content', '')
        letter = models.Template.objects.get(title=template_data)
        content = Template(letter.content).render(
            Context({
                'username': content_data.get('username', ''),
                'email': content_data.get('email', ''),
                'phone': content_data.get('phone', ''),
                'invoice_id': content_data.get('invoice_id', ''),
                'invoice_number': content_data.get('invoice_number', ''),
                'invoice_date': content_data.get('invoice_date', ''),
                'reporting_period': content_data.get('reporting_period', ''),
                'link': content_data.get('link', ''),
            }))
        notification_serializer = {}
        template = models.Template.objects.filter(title=template_data).first()
        notification_serializer['template'] = template.pk
        notification_serializer['username'] = content_data.get('username', '')
        notification_serializer['email'] = content_data.get('email', '')
        notification_serializer['phone'] = content_data.get('phone', '')
        notification_serializer['invoice_id'] = content_data.get('invoice_id', '')
        notification_serializer['invoice_number'] = content_data.get('invoice_number', '')
        notification_serializer['invoice_date'] = content_data.get('invoice_date', '')
        notification_serializer['reporting_period'] = content_data.get('reporting_period', '')
        notification_serializer['link'] = content_data.get('link', '')
        serializer_data = serializers.NotificationSerializer(
            data=notification_serializer
        )

        if serializer_data.is_valid():
            preference = models.Preference.objects.first() or {}
            if template.is_notification_email:
                subject=[
                    x[1] for x in models.Template.TEMPLATE_CHOICES if x[0] == template.title
                ]
                message = Mail(
                    from_email=preference.email,
                    to_emails=content_data['email'],
                    subject=subject[0],
                    html_content=content)
                try:
                    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(message)
                    # print(response.status_code)
                    # print(response.body)
                    # print(response.headers)
                    message_id = response.headers.get('X-Message-Id')
                    logger.info(
                        'send email: {}'.format(
                            'Письмо успешно отправленно: {}'.format(
                                content_data['email'])))
                except Exception as e:
                    print(e.message)
                    logger.error(
                        'send email: {}'.format(
                            'Ошибка! Письмо на email {} не отправленно'.format(
                                content_data['email'])))

            if template.is_notification_sms:
                pass

            serializer_data.save(message_id=message_id)
            return JSONResponse(
                serializer_data.data,
                status=status.HTTP_201_CREATED)
        return JSONResponse(
            serializer_data.errors,
            status=status.HTTP_400_BAD_REQUEST)
