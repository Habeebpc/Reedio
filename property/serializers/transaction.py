from rest_framework import serializers
from property.models import (
    TransactionCategory,
    Transaction,
)


class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('created_by', 'created_date')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['user']
        return super().create(validated_data)
