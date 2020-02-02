from api import models
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class NotificationTests(APITestCase):
    """
    Уведомлендия
    """
    def setUp(self):
        self.client = APIClient()

        # данные для Preference
        self.preference_dict = {
            'email': 'test@mail.com',
            'phone': '77777777777',
            'test_email': 'django2shop@gmail.com',
            'test_phone': '88888888888',
        }
        self.preference = models.Preference.objects.create(**self.preference_dict)
        # данные для Template
        self.template_title = 'client_registration_email'
        self.template_data = {
            'title': self.template_title,
            'content': 'Для подтверждение электронной почты: {{ email }} \
                при регистрации пользователя: {{ username }} \
                пройдите по ссылке: {{ link }}',
            'is_notification_email': True,
        }
        self.template = models.Template.objects.create(**self.template_data)
        # данные для Notification
        self.client_registration_email_1 = {
            'template': self.template,
            'username': 'Иван Иванов',
            'email': 'django2shop@gmail.com',
            'link': 'http://site.com/registration/lsdhfl64dsafga/',
        }
        self.registration_1 = models.Notification.objects.create(**self.client_registration_email_1)
        # данные для запроса к api
        self.client_registration_email_request = {
            'template': 'client_registration_email',
            'content': {
                'username': 'Александр Александров',
                'email': 'django2shop@gmail.com',
                'link': 'http://site.com/registration/klghsa46gfdah/',
            }
        }

    def equal_test(self, first, second):
        """
        Сравниваем данные полученные из запроса с исходными данными.
        """
        for key in first.keys():
            self.assertEqual(first[key], second[key])

    def test_valid_data(self):
        """
        Проверяем корректность сохраненных в бд записей.
        """
        self.assertEqual(models.Notification.objects.count(), 1)
        notification = models.Notification.objects.values().get(pk=self.registration_1.pk)
        # перед проверкой удаляем поле ForeignKey
        self.assertEqual(self.client_registration_email_1.pop('template'), self.template)
        self.equal_test(self.client_registration_email_1, notification)

    def test_post_client_registration_email(self):
        """
        Проверка создания нового уведомления.
        """
        notification_count = models.Notification.objects.count()
        url_post = reverse_lazy('api:create-notification')
        # Создаем уведомления
        response_post = self.client.post(
            url_post,
            self.client_registration_email_request,
            format='json'
        )
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Notification.objects.count(), notification_count + 1)
        # Проверяем существование объекта
        response_data = response_post.json()
        notification = models.Notification.objects.values().filter(
            message_id=response_data['message_id']).first()
        self.assertEqual(self.client_registration_email_request.pop('template'), self.template_title)
        self.equal_test(self.client_registration_email_request['content'], notification)
