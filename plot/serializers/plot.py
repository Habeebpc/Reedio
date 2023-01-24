from rest_framework import serializers
from plot.models import Plot


class PlotListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        fields = '__all__'


class PlotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plot
        exclude = ('created_by', 'created_date')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['user']
        return super().create(validated_data)
