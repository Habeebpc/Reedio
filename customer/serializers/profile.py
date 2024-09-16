from rest_framework import serializers
from user_auth.models import User
from customer.models import HelpDesk
from datetime import date, timedelta


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'name',
            'email',
            'mobile',
            'gold_user',
            'diamond_user',
            'premium_expiry_date'
        )


class UpgradeToPremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('gold_user', 'diamond_user')

    def update(self, instance, validated_data):
        instance.gold_user = validated_data.get(
            'gold_user', instance.gold_user
        )
        instance.diamond_user = validated_data.get(
            'diamond_user', instance.diamond_user
        )
        today = date.today()
        instance.premium_start_date = today
        instance.premium_expiry_date = today + timedelta(days=365)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.gold_user:
            rep['message'] = 'Successfully Upgraded to gold membership'
        elif instance.diamond_user:
            rep['message'] = 'Successfully Upgraded to diamond membership'
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
