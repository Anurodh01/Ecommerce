from unicodedata import category
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
# Create your views here.
def home(request):
    return render(request,'store/index.html')

def collections(request):
    category=Category.objects.filter(status=0)
    context={'category':category}
    return render(request,'store/collections.html',context)

def collectionsview(request,slug):
    if(Category.objects.filter(slug=slug,status=0)):
        products=Product.objects.filter(category__slug=slug)
        category_name=Category.objects.filter(slug=slug).first()
        context={'product':products,'category_name':category_name}
        return render(request,'store/products/index.html',context)
    else:
        messages.warning(request,"No such category found")
        return redirect('collections')

def productview(request,cat_slug, prod_slug):
    if(Category.objects.filter(slug=cat_slug,status=0)):
        if(Product.objects.filter(slug=prod_slug,status=0)):
            products=Product.objects.filter(slug=prod_slug,status=0).first
            context={'products':products}
        else:
            messages.error("No such category found")
            return redirect('collections')

    
    else:
        messages.error("No such category found")
        return redirect('collections')
    return render(request,'store/products/view.html',context)

def searchproducts(request):
    products=Product.objects.filter(status=0).values_list('name',flat=True)
    productsitems=list(products)
    return JsonResponse(productsitems,safe=False)

def search(request):
    if request.method=="POST":
        searchitem=request.POST.get('searchproduct')
        if searchitem=="":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product=Product.objects.filter(name__contains=searchitem).first()
            if product:
                return redirect('collections/'+product.category.slug+'/'+product.slug)
            else:
                messages.error(request,"No products is matched with your search")
                return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))