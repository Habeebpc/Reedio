from rest_framework import serializers
from user_auth.models import User


class SubAdminListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if not self.instance:
            if User.objects.filter(email=attrs['email']).exists():
                raise serializers.ValidationError('Email already exists')
        return attrs

    def create(self, validated_data):
        validated_data['user_type'] = 2
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

