from django.contrib import admin
from .models import Category, Product, Customer, Sale, SaleItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'barcode')

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

class SaleAdmin(admin.ModelAdmin):
    list_display = ('reference_no', 'customer', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('reference_no', 'customer__name')
    inlines = [SaleItemInline]

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleItem)