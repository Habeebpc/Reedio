from rest_framework import serializers
from property.models import Meeting


class MeetingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'


class MeetingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        exclude = ('created_by', 'created_date')
