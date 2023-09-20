from rest_framework import serializers
from user_auth.models import User
from customer.models import HelpDesk
from datetime import datetime


class CustomersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'mobile', 'email', 'premium_user')


class QuarriesSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = HelpDesk
        fields = ('id', 'user', 'title', 'body',
                  'created_on', 'reply', 'reply_on')
        read_only_fields = ('id', 'title', 'body', 'created_on', 'reply_on')

    def get_user(self, obj):
        return CustomersListSerializer(obj.user).data

    def update(self, instance, validated_data):
        instance.is_replied = True
        instance.reply_on = datetime.now()
        return super().update(instance, validated_data)
