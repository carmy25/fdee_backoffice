from rest_framework import serializers

from .models import Receipt


class ReceiptSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    number = serializers.IntegerField()

    def create(self, validate_data):
        return Receipt.objects.create(**validate_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance
