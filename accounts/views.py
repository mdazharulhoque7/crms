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

    context = {'customers': customers,
                   'orders':orders,
                   'total_customer':total_customer,
                   'total_orders':total_orders,
                   'order_delivered':order_delivered,
                   'order_pending':order_pending,
                   }
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer,
               'orders': orders,
               'order_count': order_count,
               }
    return render(request, 'accounts/customer.html', context)
