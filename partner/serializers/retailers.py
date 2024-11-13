from rest_framework import serializers
from user_auth.models import User, PartnerAndRetailer
from retailer.models import AccessCode
from user_auth.serializers import generate_number
from decouple import config


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerAndRetailer
        fields = ('id', 'name', 'email', 'mobile')

    def validate(self, attrs):
        user = self.context.get('user')
        email = attrs.get('email').lower()
        mobile = attrs.get('mobile')

        if PartnerAndRetailer.objects.filter(
            partner=user,
            email=email,
        ).exists():
            raise serializers.ValidationError(
                'Retailer already added in this email')

        if PartnerAndRetailer.objects.filter(
            partner=user,
            mobile=mobile
        ).exists():
            raise serializers.ValidationError(
                'Retailer already added in this mobile')

        if User.objects.filter(email=email).exclude(user_type=5).exists():
            raise serializers.ValidationError('Email already exists')
        else:
            if User.objects.filter(mobile=mobile).exists():
                raise serializers.ValidationError('Mobile already exists')

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context.get('user')
        email = validated_data.get('email')

        if User.objects.filter(email=email).exists():
            retailer = User.objects.get(email=email)
        else:
            name = validated_data.get('name')
            mobile = validated_data.get('mobile')
            user_type = 5
            username = email.split('@')[0]+generate_number(5)
            password = config('SOCIAL_AUTH_PASSWORD')
            retailer = User.objects.create_user(
                name=name,
                email=email,
                mobile=mobile,
                user_type=user_type,
                username=username,
                password=password
            )

        validated_data['partner'] = user
        validated_data['retailer'] = retailer
        validated_data['is_active'] = True

        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['is_active'] = instance.is_active
        return rep


class RetailerStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerAndRetailer
        fields = ('is_active',)


class AccessCodeEnrolledSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.name')
    date = serializers.DateTimeField(source='created_on')
    podcast = serializers.CharField(source='podcast.name')
    redeemed_by = serializers.SerializerMethodField()

    class Meta:
        model = AccessCode
        fields = (
            'id',
            'created_by',
            'date',
            'podcast',
            'code',
            'sent_to',
            'redeemed_by'
        )

    def get_redeemed_by(self, obj):
        return {
            'name': obj.redeemed_by.name,
            'mobile': obj.redeemed_by.mobile,
            'date': obj.redeemed_on
        } if obj.redeemed_by else None
