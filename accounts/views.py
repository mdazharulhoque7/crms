from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

# Create your views here.
from .models import Product, Order, Customer
from .forms import OrderForm
from .filters import OrderFilter

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
    orderFilter = OrderFilter(request.GET, queryset=orders)
    orders = orderFilter.qs
    order_count = orders.count()
    context = {'customer': customer,
               'orders': orders,
               'orderFilter': orderFilter,
               'order_count': order_count,
               }
    return render(request, 'accounts/customer.html', context)

def createOrder(request, customer_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=10)
    customer = Customer.objects.get(pk=customer_id)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    contex = {'formset': formset}
    return render(request, 'accounts/order_form.html', contex)

def updateOrder(request, id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    contex = {'form': form}
    return render(request, 'accounts/order_form.html', contex)

def deleteOrder(request, id):
    order = Order.objects.get(id=id)

    if request.method == 'POST':
        order.delete()
        return redirect('/')
    contex = {'item': order}
    return render(request, 'accounts/delete.html', contex)