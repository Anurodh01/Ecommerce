
from store.models import Cart, Order, OrderItem, Product, Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators  import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

def orders(request):
    orders=Order.objects.filter(user=request.user)
    context={'orders':orders}
    return render(request,'store/orders/index.html',context)

def orderview(request, t_no):
    order= Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems=OrderItem.objects.filter(order=order)
    context={'order':order,'orderitems':orderitems}
    return render(request,'store/orders/view.html',context)