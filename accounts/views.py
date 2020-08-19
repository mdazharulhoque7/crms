from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .models import Product, Order, Customer

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()
    total_orders = orders.count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()

    return render(request, 'accounts/dashboard.html',
                  {'customers': customers,
                   'orders':orders,
                   'total_customer':total_customer,
                   'total_orders':total_orders,
                   'order_delivered':order_delivered,
                   'order_pending':order_pending,
                   })

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customer(request):
    return render(request, 'accounts/customer.html')
