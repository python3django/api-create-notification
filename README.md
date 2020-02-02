# API для микросервиса CreateNotification.
---

* Python 3, Django 3

* после запуска виртуальной среды (например:  source .env/bin/activate), необходимо добавить в неё ключ для api почтового сервиса sendgrid выполнив: source sendgrid.env

* api_db.json - дамп приложения api для быстрого тестирования

* создание сообщения в программе httpie:

http POST 127.0.0.1:8000/api/v1/notification/ template="client_registration_email" \
content:='{"username": "Man5", "email": "django2shop@gmail.com", \
"link": "http://site.com/registration/abcdfegkl/"}'

http POST 127.0.0.1:8000api/v1/notification/ template="client_invoice_email" \
content:='{"username": "Man5", "email": "django2shop@gmail.com", \
"link": "http://site.com/invoice/abcdfegkl/", "invoice_id": "afdadf6546", \
"invoice_number": "5", "invoice_date": "01 февраля 2020", \
"reporting_period": "c 01 января 2020 по 31 января 2020"}'

* тесты:
python manage.py test
