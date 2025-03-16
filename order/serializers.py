from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


from place.models import Place

from .models import ProductItem, Receipt, Product, Category


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.SlugRelatedField('name', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category')

    def get_category(self, obj):
        splited_name = obj.category.full_name.split('->')
        if len(splited_name) == 1:
            return splited_name[0]
        return splited_name[1]


class CategoryProductsSerializer(CategorySerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'parent', 'products']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category')

    def get_category(self, obj):
        splited_name = obj.category.full_name.split('->')
        if len(splited_name) == 1:
            return splited_name[0]
        return splited_name[1]


class ProductItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductItem
        fields = (
            'product_type', 'amount', 'name', 'price'
        )

    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        return obj.product_type.price

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['name']:
            data['name'] = instance.product_type.name
        return data


class ReceiptSerializer(WritableNestedModelSerializer):
    place = serializers.PrimaryKeyRelatedField(
        queryset=Place.objects.all(),
        required=False,
        allow_null=True
    )
    product_items = ProductItemSerializer(many=True)
    place_name = serializers.SlugRelatedField(
        read_only=True, source='place', slug_field='name')

    class Meta:
        model = Receipt
        fields = (
            'id', 'status',
            'place', 'number', 'created_at', 'payment_method',
            'price', 'product_items', 'place_name'
        )

    def create(self, validated_data):
        product_items_data = validated_data.pop('product_items')
        receipt = Receipt.objects.create(**validated_data)
        for product_item_data in product_items_data:
            ProductItem.objects.create(receipt=receipt, **product_item_data)
        return receipt

    # def update(self, instance, validated_data):
    #     instance.save()
    #     return instance
