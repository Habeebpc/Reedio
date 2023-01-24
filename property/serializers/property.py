from rest_framework import serializers
from property.models import Property


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ('created_by', 'created_date')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['user']
        return super().create(validated_data)
