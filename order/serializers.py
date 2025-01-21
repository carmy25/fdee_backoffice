from rest_framework import serializers

from place.serializers import PlaceSerializer

from .models import Receipt, Product, Category


class ReceiptSerializer(serializers.Serializer):
    class Meta:
        model = Receipt


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'top_category_name']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_category(self, obj):
        splited_name = obj.category.full_name.split('->')
        if len(splited_name) == 1:
            return splited_name[0]
        return splited_name[1]


class ReceiptSerializer(serializers.ModelSerializer):
    place = PlaceSerializer(read_only=True)

    class Meta:
        model = Receipt
        fields = (
            'id',
            'place', 'number', 'created_at', 'payment_method',
            'price',
        )
