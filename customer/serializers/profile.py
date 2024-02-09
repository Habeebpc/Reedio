from rest_framework import serializers
from user_auth.models import User
from customer.models import HelpDesk
from datetime import date, timedelta


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'mobile', 'premium_user')


class UpgradeToPremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ()

    def update(self, instance, validated_data):
        instance.premium_user = True
        today = date.today()
        instance.premium_start_date = today
        instance.premium_expiry_date = today + timedelta(days=365)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['message'] = 'Successfully Upgraded To Premium'
        return rep


class HelpDeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpDesk
        fields = ('id', 'title', 'body',  'created_on', 'reply', 'reply_on')
        read_only_fields = ('id', 'created_on', 'reply', 'reply_on')

    def validate(self, attrs):
        if self.instance and self.instance.is_replied:
            raise serializers.ValidationError("cant edit replied queries")
        return super().validate(attrs)
