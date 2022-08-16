from itertools import product
from store.models import Cart, Product
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .authview import loginpage

def addtocart(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            prod_id=request.POST.get('product_id')
            print(prod_id)
            product_check=Product.objects.get(id=prod_id)
            if(product_check):
                if Cart.objects.filter(user=request.user, product=product_check):
                    return JsonResponse({'status':'Product already in cart'})
                else:
                    prod_qty=int(request.POST.get('product_qty'))
                    print(prod_qty)
                    if product_check.quantity >= prod_qty:
                        Cart.objects.create(user=request.user,product_id=prod_id,product_pty=prod_qty)
                        return JsonResponse({'status':'Product added successfully'})
                    else:
                        return JsonResponse({'status':" Only "+ str(product_check.quantity)+ "quantity available."})
            else:
                return JsonResponse({'status':'No such Product found'})

        else:
            return JsonResponse({"status": "Login to continue"})
    else:
        return redirect('home')

@login_required(login_url='login')
def viewcart(request):
    cart=Cart.objects.filter(user=request.user)
    context={'cart':cart}
    return render(request,'store/cart.html',context)

def updatecart(request):
    if request.method=="POST":
        prod_id=request.POST.get('product_id')
        prod_qty=request.POST.get('product_qty')
        if(Cart.objects.get(user=request.user,product_id=prod_id)):
            cart=Cart.objects.get(user=request.user, product_id=prod_id)
            cart.product_pty=prod_qty
            print(cart.product_pty)
            cart.save()
            return JsonResponse({'status':'Updated Successfully.'})
    return redirect('home')


def deletecartitem(request):
    prod_id=request.POST.get('product_id')
    if(Cart.objects.filter(user=request.user,product_id=prod_id)):
        cartitem=Cart.objects.get(user=request.user,product_id=prod_id)
        cartitem.delete()
        return JsonResponse({'status':'Item Deleted Successfully'})
    return redirect('home')