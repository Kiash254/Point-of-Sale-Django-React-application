
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_user, name='register'),
    path('profile/', views.user_profile, name='profile'),
    
    # Categories
    path('categories/', views.category_list, name='category-list'),
    path('categories/<int:pk>/', views.category_detail, name='category-detail'),
    
    # Products
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/category/<int:category_id>/', views.products_by_category, name='products-by-category'),
    path('products/search/', views.product_search, name='product-search'),
    
    # Customers
    path('customers/', views.customer_list, name='customer-list'),
    path('customers/<int:pk>/', views.customer_detail, name='customer-detail'),
    path('customers/search/', views.customer_search, name='customer-search'),
    
    # Sales
    path('sales/', views.sale_list, name='sale-list'),
    path('sales/<int:pk>/', views.sale_detail, name='sale-detail'),
    path('sales/create/', views.create_sale, name='sale-create'),
    
    # Dashboard
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('dashboard/sales/daily/', views.daily_sales, name='daily-sales'),
    path('dashboard/sales/weekly/', views.weekly_sales, name='weekly-sales'),
    path('dashboard/sales/monthly/', views.monthly_sales, name='monthly-sales'),
]