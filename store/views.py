from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *


# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer=customer)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def add_to_cart(request, product):
    prod = get_object_or_404(Product, id=product)
    customer = request.user.customer
    order = Order.objects.get(customer=customer)
    orderItem = OrderItem.objects.create(product=prod, order=order)
    orderItem.quantity += 1
    orderItem.save()
    return HttpResponseRedirect('/store/')


def delete_to_cart(request, item):
    orderItem = OrderItem.objects.get(id=item)
    customer = request.user.customer
    order = Order.objects.get(customer=customer)
    items = order.orderitem_set.all()

    context = {'items': items, 'order': order}
    orderItem.quantity -= 1
    if orderItem.quantity > 0:
        orderItem.save()
    else:
        orderItem.delete()
    return render(request, 'store/cart.html', context)
