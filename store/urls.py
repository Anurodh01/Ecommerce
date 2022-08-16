from store.models import Wishlist
from django.urls import path
# from matplotlib import collections
from . import views
from store.controller import authview, cart, wishlist ,checkout, order
# from django.contrib.auth import views as  auth_views
urlpatterns=[
    path('',views.home,name='home'),
    path('collections/',views.collections,name='collections'),
    path('collections/<str:slug>',views.collectionsview,name='collectionsview'),
    path('collections/<str:cat_slug>/<str:prod_slug>', views.productview, name="productview"),
    path('register/',authview.register,name='register'),
    path('login/',authview.loginpage,name='login'),
    path('logout/',authview.logoutpage,name="logout"),

    #Cart
    path('add-to-cart',cart.addtocart,name='addtocart'),
    path('cart/',cart.viewcart,name='cart'),
    path('update-cart-item',cart.updatecart,name='updatecart'),
    path('delete-cart-item',cart.deletecartitem,name='deletecartitem'),

    #wishlist
    path('wishlist',wishlist.index,name='wishlist'),
    path('add-to-wishlist',wishlist.addtowishlist,name='addtowishlist'),
    path('delete-wishlist-item',wishlist.deletewishlistitem,name='deletewishlistitem'),

    #checkout
    path('checkout',checkout.index,name='checkout'),
    path('placeorder',checkout.placeorder,name='placeorder'),
    path('proceed-to-pay',checkout.razorpaycheck,name='razorpaycheck'),

    #orders
    path('my-orders',order.orders,name='orders'),
    path('view-order/<str:t_no>',order.orderview,name='orderview'),

    #search_bar
    path('product-list',views.searchproducts),
    path('search',views.search,name='search'),
]

