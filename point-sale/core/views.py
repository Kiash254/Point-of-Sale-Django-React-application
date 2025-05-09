from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, Product, Customer, Sale, SaleItem
from .serializers import (
    UserSerializer, CategorySerializer, ProductSerializer,
    CustomerSerializer, SaleSerializer, SaleCreateSerializer
)

# Authentication views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    if not username or not password or not email:
        return Response(
            {'error': 'Username, password, and email are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get or update user profile"""
    user = request.user
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        
        if 'password' in request.data:
            user.set_password(request.data['password'])
        
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Category views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def category_list(request):
    """List all categories or create a new one"""
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    """Retrieve, update or delete a category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Product views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list(request):
    """List all products or create a new one"""
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    """Retrieve, update or delete a product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def products_by_category(request, category_id):
    """List all products by category"""
    products = Product.objects.filter(category_id=category_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_search(request):
    """Search for products by name, barcode, or category"""
    query = request.query_params.get('q', '')
    products = Product.objects.filter(name__icontains=query) | \
               Product.objects.filter(barcode__icontains=query)
    
    category = request.query_params.get('category', '')
    if category:
        products = products.filter(category_id=category)
    
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# Customer views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def customer_list(request):
    """List all customers or create a new one"""
    if request.method == 'GET':
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def customer_detail(request, pk):
    """Retrieve, update or delete a customer"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'GET':
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_search(request):
    """Search for customers by name, email, or phone"""
    query = request.query_params.get('q', '')
    customers = Customer.objects.filter(name__icontains=query) | \
                Customer.objects.filter(email__icontains=query) | \
                Customer.objects.filter(phone__icontains=query)
    
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# Sale views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sale_list(request):
    """List all sales"""
    sales = Sale.objects.all().order_by('-created_at')
    
    # Filter by date range if provided
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    if start_date and end_date:
        sales = sales.filter(created_at__range=[start_date, end_date])
    
    # Filter by status if provided
    status_param = request.query_params.get('status')
    if status_param:
        sales = sales.filter(status=status_param)
    
    # Pagination
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))
    start = (page - 1) * page_size
    end = start + page_size
    
    count = sales.count()
    sales = sales[start:end]
    
    serializer = SaleSerializer(sales, many=True)
    return Response({
        'count': count,
        'results': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sale_detail(request, pk):
    """Retrieve sale details"""
    sale = get_object_or_404(Sale, pk=pk)
    serializer = SaleSerializer(sale)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_sale(request):
    """Create a new sale with items"""
    data = request.data.copy()
    data['user'] = request.user.id
    
    serializer = SaleCreateSerializer(data=data)
    if serializer.is_valid():
        sale = serializer.save(user=request.user)
        
        # Return the created sale with all details
        response_serializer = SaleSerializer(sale)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Dashboard views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics"""
    today = timezone.now().date()
    
    # Get today's sales
    today_sales = Sale.objects.filter(
        created_at__date=today,
        status='COMPLETED'
    )
    today_sales_count = today_sales.count()
    today_sales_amount = today_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Get total products, categories, and customers
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_customers = Customer.objects.count()
    
    # Get low stock products (less than 10 items)
    low_stock = Product.objects.filter(stock__lt=10).count()
    
    # Get top selling products
    top_products = SaleItem.objects.filter(
        sale__status='COMPLETED'
    ).values('product__name').annotate(
        sold=Sum('quantity')
    ).order_by('-sold')[:5]
    
    return Response({
        'today_sales_count': today_sales_count,
        'today_sales_amount': today_sales_amount,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_customers': total_customers,
        'low_stock': low_stock,
        'top_products': top_products
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def daily_sales(request):
    """Get daily sales for the last 7 days"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    
    sales_data = []
    current_date = start_date
    
    while current_date <= end_date:
        day_sales = Sale.objects.filter(
            created_at__date=current_date,
            status='COMPLETED'
        )
        amount = day_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        count = day_sales.count()
        
        sales_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'day': current_date.strftime('%a'),
            'amount': amount,
            'count': count
        })
        
        current_date += timedelta(days=1)
    
    return Response(sales_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_sales(request):
    """Get weekly sales for the last 4 weeks"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=28)
    
    sales_data = []
    current_date = start_date
    
    for week in range(4):
        week_end = current_date + timedelta(days=6)
        week_sales = Sale.objects.filter(
            created_at__date__range=[current_date, week_end],
            status='COMPLETED'
        )
        amount = week_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        count = week_sales.count()
        
        sales_data.append({
            'week': f'Week {week + 1}',
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': week_end.strftime('%Y-%m-%d'),
            'amount': amount,
            'count': count
        })
        
        current_date += timedelta(days=7)
    
    return Response(sales_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_sales(request):
    """Get monthly sales for the last 6 months"""
    current_date = timezone.now().date()
    
    sales_data = []
    for i in range(6):
        # Calculate first and last day of the month
        month = current_date.month - i
        year = current_date.year
        
        # Adjust year if needed
        if month <= 0:
            month += 12
            year -= 1
        
        # Get sales for this month
        month_sales = Sale.objects.filter(
            created_at__year=year,
            created_at__month=month,
            status='COMPLETED'
        )
        
        amount = month_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        count = month_sales.count()
        
        month_name = timezone.datetime(year, month, 1).strftime('%B %Y')
        
        sales_data.append({
            'month': month_name,
            'amount': amount,
            'count': count
        })
    
    # Reverse to get chronological order
    sales_data.reverse()
    
    return Response(sales_data)