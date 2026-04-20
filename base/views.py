from operator import truth
from django.shortcuts import render,redirect
from .models import Products,CartModel,Order
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404



# Create your views here.
def home(request):
    if request.user.is_authenticated:
        cartproductscount = CartModel.objects.filter(host=request.user).count()
    else:
        cartproductscount = False

    nomatch = False
    trend = False
    offer = False

    if 'q' in request.GET:
        q = request.GET['q']
        all_products = Products.objects.filter(Q(pname__icontains = q)| Q(pdesc__icontains=q))
        print(len(all_products))#0 #2
        if len(all_products) == 0:
            nomatch=True
    elif 'cat' in request.GET:
        cat = request.GET['cat']
        all_products = Products.objects.filter(pcategory = cat)
    elif 'trending' in request.GET:
        all_products = Products.objects.filter(trending = True)
        trend = True
    elif 'offer' in request.GET:
        all_products = Products.objects.filter(offer = True)
        offer = True
    else:
        all_products = Products.objects.all()
    
    list = [] #empty list
    data = Products.objects.all()
    for i in data:#fletching all records 
        if i.pcategory not in list:
            list+=[i.pcategory]

    return render(request,'home.html',{'all_products':all_products,'cartproductscount':cartproductscount,'nomatch':nomatch,'category':list,'trend':trend,'offer':offer})

@login_required(login_url='login_')
def addtocart(request,pk):
    product = Products.objects.get(id=pk)

    try:
        cp = CartModel.objects.get(pname = product.pname,host = request.user)
        cp.quatity+=1
        cp.totalprice+=product.price
        cp.save()
        return redirect('home')
    except:
        CartModel.objects.create(
            pname = product.pname,
            price = product.price,
            pcategory = product.pcategory,
            quatity  = 1,
            totalprice = product.price,
            host = request.user
        )
        messages.success(request,"Product added to cart 🛒")
        return redirect('home')

def cart(request):
    cartproductscount = CartModel.objects.filter(host=request.user).count()
    cartproducts = CartModel.objects.filter(host=request.user)

    TA = 0
    for i in cartproducts:
        # print(i.totalprice)
        TA+=i.totalprice
    print(TA)
    return render(request,'cart.html',{'cartproducts':cartproducts,'TA':TA,'cartproductscount':cartproductscount,'profile_nav':True})

def remove(request,pk):
    data = CartModel.objects.get(id=pk)
    data.delete()
    messages.warning(request,"Item removed from cart ❌")
    return redirect('cart')

def sub(request,pk):
    cproduct = CartModel.objects.get(id=pk)
    if cproduct.quatity >1:
        cproduct.quatity-=1
        cproduct.totalprice-=cproduct.price
        cproduct.save()
        messages.info(request,"Quantity decreased ➖") 
    else:
        cproduct.delete()
        messages.warning(request,"Item removed from cart ❌")
    return redirect('cart')

def add(request,pk):
    cproduct = CartModel.objects.get(id=pk)
    cproduct.quatity+=1
    cproduct.totalprice+=cproduct.price
    cproduct.save()
    messages.info(request,"Quantity increased ➕") 
    return redirect('cart')


@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    cartproductscount = CartModel.objects.filter(host=request.user).count()

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders,
            "cartproductscount": cartproductscount,
            "profile_nav": True
        }
    )

# ===============================
# checkout() VIEW
# ===============================

@login_required
def checkout(request):

    cart_items = CartModel.objects.filter(host=request.user)

    total_amount = 0

    for item in cart_items:
        total_amount += item.totalprice

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": total_amount * 100,
        "currency": "INR",
        "payment_capture": "1"
    })

    request.session["cart_checkout"] = True

    return render(
        request,
        "checkout.html",
        {
            "payment": payment,
            "amount": total_amount,
            "key": settings.RAZORPAY_KEY_ID
        }
    )


# ===============================
# BUY NOW SINGLE PRODUCT
# ===============================

@login_required
def buy_now(request, pk):

    product = get_object_or_404(Products, id=pk)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    payment = client.order.create({
        "amount": product.price * 100,
        "currency": "INR",
        "payment_capture": "1"
    })

    request.session["buy_product_id"] = product.id

    return render(
        request,
        "checkout.html",
        {
            "payment": payment,
            "amount": product.price,
            "key": settings.RAZORPAY_KEY_ID,
            "product": product
        }
    )


# ===============================
# PAYMENT SUCCESS
# ===============================

@login_required
def payment_success(request):

    # ---------------------------
    # CART CHECKOUT
    # ---------------------------
    if request.session.get("cart_checkout"):

        cart_items = CartModel.objects.filter(host=request.user)

        for item in cart_items:

            Order.objects.create(
                user=request.user,
                product=Products.objects.get(pname=item.pname),
                quantity=item.quatity,
                price=item.totalprice
            )

        cart_items.delete()

        del request.session["cart_checkout"]

        messages.success(
            request,
            "Order placed successfully 🎉"
        )

        return redirect("my_orders")

    # ---------------------------
    # BUY NOW SINGLE PRODUCT
    # ---------------------------
    elif request.session.get("buy_product_id"):

        product_id = request.session["buy_product_id"]

        product = Products.objects.get(id=product_id)

        Order.objects.create(
            user=request.user,
            product=product,
            quantity=1,
            price=product.price
        )

        del request.session["buy_product_id"]

        messages.success(
            request,
            "Product purchased successfully 🎉"
        )

        return redirect("my_orders")

    return redirect("home")

def knowus(request):
    return render(request, 'knowus.html')

def support(request):
    return render(request, 'support.html')
