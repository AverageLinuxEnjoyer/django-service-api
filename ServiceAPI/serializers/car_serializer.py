from rest_framework import serializers
from ..models.car import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ['total_workmanship']

    def create(self):
        return Car(**self.validated_data)
