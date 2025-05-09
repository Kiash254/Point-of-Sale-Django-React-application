
# pos_app/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Customer, Sale, SaleItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'description', 
                  'price', 'stock', 'image', 'barcode', 'created_at', 'updated_at']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Sale
        fields = ['id', 'reference_no', 'customer', 'customer_name', 'user', 
                  'user_name', 'status', 'total_amount', 'paid_amount', 
                  'change_amount', 'payment_method', 'notes', 'created_at', 
                  'updated_at', 'items']

class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ['customer', 'status', 'total_amount', 'paid_amount', 
                  'change_amount', 'payment_method', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Update stock
            product.stock -= quantity
            product.save()
            
            SaleItem.objects.create(sale=sale, **item_data)
        
        return sale
