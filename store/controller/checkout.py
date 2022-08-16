from math import prod
from statistics import fmean
from store.models import Cart, Order, OrderItem, Product, Profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators  import login_required
import random
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse

@login_required(login_url='login')
def index(request):
    rawcart=Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_pty > item.product.quantity:
            deleteitem=Cart.objects.filter(id=item.id)
            deleteitem.delete()
    cartitems=Cart.objects.filter(user=request.user)
    total_price=0
    userprofile=Profile.objects.filter(user=request.user).first()
    for item in cartitems:
        total_price+=item.product.selling_price*item.product_pty
    context={'cartitems':cartitems,'total_price':total_price,'userprofile':userprofile}
    return render(request,'store/checkout.html',context)

@login_required(login_url='login')
def placeorder(request):
    if(request.method=="POST"):
        
        if not Profile.objects.filter(user=request.user):
            newprofile=Profile()
            newprofile.user=request.user
            newprofile.phone=request.POST.get('phone')
            newprofile.address= request.POST.get('address')
            newprofile.city= request.POST.get('city')
            newprofile.state=request.POST.get('state')
            newprofile.country=request.POST.get('country')
            newprofile.pincode=request.POST.get('pincode')
            newprofile.save()
        if not request.user.first_name:
            currentuser=User.objects.filter(id=request.user.id).first()
            fname=request.POST.get('fname')
            lname=request.POST.get('lname')
            currentuser.first_name=fname
            currentuser.last_name=lname
            currentuser.save()


        neworder=Order()
        neworder.user =request.user
        neworder.fname=request.POST.get('fname')
        neworder.lname=request.POST.get('lname')
        neworder.email=request.POST.get('email')
        neworder.phone=request.POST.get('phone')
        neworder.address=request.POST.get('address')
        neworder.city=request.POST.get('city')
        neworder.state=request.POST.get('state')
        neworder.country=request.POST.get('country')
        neworder.pincode=request.POST.get('pincode')
        neworder.payment_mode=request.POST.get('payment_mode')
        neworder.payment_id=request.POST.get('payment_id')
        
        cart=Cart.objects.filter(user=request.user)
        total_price=0
        for item in cart:
            total_price += item.product_pty* item.product.selling_price
        neworder.total_price=total_price
        trackno="anurodh"+str(random.randint(11111,99999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno= "anurodh"+str(random.randint(11111,99999))
        neworder.tracking_no=trackno
        neworder.save()

        neworderitems=Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_pty
            )

            orderproduct=Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_pty
            orderproduct.save()

        #to clear users cart
        Cart.objects.filter(user=request.user).delete()
        messages.success(request,"Your order has been placed successfully")
        paymode=request.POST.get('payment_mode')
        if paymode=="Paid by Razorpay":
            return JsonResponse({'status':'Your order has been placed successfully'})
        else:
            messages.success(request,"Your order has been placed successfully")
    else:
        return redirect('home')


@login_required(login_url='login')
def razorpaycheck(request):
    cart=Cart.objects.filter(user=request.user)
    total_price=0
    for item in cart:
        total_price=total_price+ item.product.selling_price * item.product_pty
    return JsonResponse(
        {
        'total_price' : total_price
    })

def orders(request):
    return HttpResponse("My orders page")
