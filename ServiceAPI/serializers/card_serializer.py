from rest_framework import serializers
from ..models.card import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ['total_discounts']

    def create(self):
        return Card(**self.validated_data)
