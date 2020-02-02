from rest_framework import serializers

from . import models


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = [
            'template',
            'username',
            'email',
            'phone',
            'link',
            'invoice_id',
            'invoice_number',
            'invoice_date',
            'reporting_period',
            'message_id',
        ]
