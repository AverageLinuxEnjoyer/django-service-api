from rest_framework import serializers
from ..models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self):
        return Transaction(**self.validated_data)
