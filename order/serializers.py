from rest_framework import serializers

from .models import Receipt, Product, Category


class ReceiptSerializer(serializers.Serializer):
    class Meta:
        model = Receipt


class CategorySerializer(serializers.ModelSerializer):
    top_category_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'top_category_name']

    def get_top_category_name(self, obj):
        splited_name = obj.full_name.split('->')
        if len(splited_name) == 1:
            return splited_name[0]
        return splited_name[1]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'
