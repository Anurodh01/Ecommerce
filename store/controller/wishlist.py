from store.models import Wishlist
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Wishlist 

@login_required(login_url='login')
def index(request):
    wishlistitems=Wishlist.objects.filter(user=request.user)
    context={'wishlistitems': wishlistitems}
    return render(request,'store/wishlist.html',context)


def addtowishlist(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            prod_id=request.POST.get('product_id')
            if Wishlist.objects.filter(user=request.user,product_id=prod_id):
                return JsonResponse({'status':'Product is already in wishlist'})
            else:
                Wishlist.objects.create(user=request.user,product_id=prod_id)
                return JsonResponse({'status':'Product has been added to wishlist successfully'})
        else:
            return JsonResponse({'status':'Login to Continue'})
    return redirect('home')

def deletewishlistitem(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            prod_id=request.POST.get('product_id')
            if Wishlist.objects.filter(user=request.user,product_id=prod_id):
                wishlistitem=Wishlist.objects.filter(user=request.user, product_id=prod_id)
                wishlistitem.delete()
                return JsonResponse({'status':'Product has been removed successfully'})
            else:
                return JsonResponse({'status':'No such product in wishlist'})
        else:
            return JsonResponse({'status':'Login to continue'})

    return redirect('home')