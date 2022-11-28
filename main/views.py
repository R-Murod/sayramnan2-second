from math import ceil

from django.http import JsonResponse
from django.shortcuts import render, redirect
from main.models import *
from datetime import datetime


# Create your views here.


def indexHandler(request):
    categories = Category.objects.all()

    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    main_slider = Product.objects.filter(is_new=True)
    all_products = Product.objects.all()

    return render(request, 'index-3.html', {
        'categories': categories,
        'new_cart': new_cart,
        'cart_items': cart_items,
        'main_slider': main_slider,
        'all_products': all_products,
    })


def get_item(request):
    product_id = int(request.GET.get('product_id', 0))
    good_item = Product.objects.get(id=product_id)
    return JsonResponse({'good_item': {
        'title': good_item.title,
        'logo': "/media/" + str(good_item.logo),
        'logo2': "/media/" + str(good_item.logo2),
        'logo3': "/media/" + str(good_item.logo3),
        'logo4': "/media/" + str(good_item.logo4),
        'price': good_item.price,
        'old-price': good_item.old_price,
        'mini-description': good_item.mini_description,
        'size': good_item.size.title,
        'rating': good_item.rating

    }}, status=200)


def catalogHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'catalog.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
    })


def allCatalogHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    len_products = len(products)

    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'catalog-error.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
        'len_products': len_products,
    })


def catalogItemHandler(request, catalog_id):
    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    categories = Category.objects.all()
    products = Product.objects.filter(category__id=catalog_id)
    active_category = Category.objects.get(id=catalog_id)

    limit = int(request.GET.get('limit', 3))
    current_page = int(request.GET.get('page', 1))
    total = len(products)
    pages_count = ceil(total / limit)
    pages = range(1, pages_count + 1)
    stop = current_page * limit
    start = stop - limit
    prev_page = current_page - 1
    next_page = None
    if current_page < pages_count:
        next_page = current_page + 1

    return render(request, 'catalog.html', {
        'categories': categories,
        'products': products[start:stop],
        'active_category': active_category,
        'pages': pages,
        'current_page': current_page,
        'prev_page': prev_page,
        'next_page': next_page,
        'start': start,
        'stop': stop,
        'total': total,
        'new_cart': new_cart,
        'cart_items': cart_items,
    })


def productHandler(request, product_id):
    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)
    categories = Category.objects.all()
    active_product = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(category__id=active_product.category.id).exclude(id=product_id)

    return render(request, 'product-details.html', {
        'categories': categories,
        'active_product': active_product,
        'related_products': related_products,
        'new_cart': new_cart,
        'cart_items': cart_items,
    })


def cartHandler(request):
    categories = Category.objects.all()

    if not request.session.session_key:
        request.session.create()
    user_session_id = request.session.session_key

    open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
    new_cart = None
    if open_carts:
        new_cart = open_carts[0]
    else:
        new_cart = Cart()
        new_cart.session_id = user_session_id
        new_cart.save()

    if request.POST:
        return_url = request.POST.get('return_url', '')
        action = request.POST.get('action', '')

        if action == 'add_to_cart':
            product_id = int(request.POST.get('product_id', 0))
            amount = float(request.POST.get('amount', 0))

            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0).filter(product__id=product_id)
            if cart_items:
                new_cart_item = cart_items[0]
                new_cart_item.amount = new_cart_item.amount + amount
                new_cart_item.all_price = new_cart_item.price * new_cart_item.amount
                new_cart_item.save()
            else:
                new_cart_item = CartItem()
                new_cart_item.product_id = product_id
                new_cart_item.cart_id = new_cart.id
                new_cart_item.amount = amount
                new_cart_item.price = new_cart_item.product.price
                new_cart_item.all_price = new_cart_item.price * new_cart_item.amount
                new_cart_item.save()

        if action == 'remove_from_cart':
            product_id = int(request.POST.get('product_id', 0))
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0).filter(product__id=product_id)
            for ci in cart_items:
                ci.delete()

        if action == 'clear_cart':
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)
            for ci in cart_items:
                ci.delete()

        if action == 'checkout':
            new_cart.comment = request.POST.get('comment', '')
            new_cart.first_name = request.POST.get('first_name', '')
            new_cart.last_name = request.POST.get('last_name', '')
            new_cart.country = request.POST.get('country', '')
            new_cart.city = request.POST.get('city', '')
            new_cart.address = request.POST.get('address', '')
            new_cart.zip_code = request.POST.get('zip_code', '')
            new_cart.phone = request.POST.get('phone', '')
            new_cart.email = request.POST.get('email', '')
            new_cart.created_at = datetime.now()
            new_cart.status = 1
            new_cart.save()

        if action == 'accepted':
            order_id = int(request.POST.get('order_id', 0))
            if request.user.is_authenticated:
                main_order = Cart.objects.get(id=order_id)
                if main_order:
                    main_order.status = 2
                    main_order.save()

        if action == 'subscriber':
            email = request.POST.get('email', '')
            if email:
                subscriber_list = Subscriber.objects.filter(email=email)
                if not subscriber_list:
                    subscriber = Subscriber()
                    subscriber.email = email
                    subscriber.save()

        if action == 'add_to_compare_list':
            product_id = int(request.POST.get('product_id', 0))
            compare_item = CompareItem.objects.filter(product__id=product_id).filter(session_id=user_session_id)
            if compare_item:
                pass
            else:
                new_compare_item = CompareItem()
                new_compare_item.session_id = user_session_id
                new_compare_item.product_id = product_id
                new_compare_item.save()

        if action == 'add_to_wish_list':
            product_id = int(request.POST.get('product_id', 0))
            wish_item = WishItem.objects.filter(product__id=product_id).filter(session_id=user_session_id)
            if wish_item:
                pass
            else:
                new_wish_item = WishItem()
                new_wish_item.session_id = user_session_id
                new_wish_item.product_id = product_id
                new_wish_item.save()

        if action == 'remove_from_compare_list':
            product_id = int(request.POST.get('product_id', 0))
            compare_item = CompareItem.objects.filter(product__id=product_id).filter(session_id=user_session_id)
            if compare_item:
                for ci in compare_item:
                    ci.delete()

        if action == 'remove_from_wish_list':
            product_id = int(request.POST.get('product_id', 0))
            wish_item = WishItem.objects.filter(product__id=product_id).filter(session_id=user_session_id)
            if wish_item:
                for ci in wish_item:
                    ci.delete()

        if action in ['add_to_cart', 'remove_from_cart', 'clear_cart']:
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)
            all_price = 0
            all_amount = 0
            all_orig_price = 0
            if cart_items:
                for ci in cart_items:
                    all_amount += ci.amount
                    all_orig_price += ci.amount * ci.price

            all_price = all_orig_price * (100 - new_cart.discount) / 100
            new_cart.amount = all_amount
            new_cart.orig_price = all_orig_price
            new_cart.price = all_price
            new_cart.save()

        if return_url:
            return redirect(return_url)

    cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'cart.html', {
        'categories': categories,
        'new_cart': new_cart,
        'cart_items': cart_items,
    })


def checkoutHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'checkout.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
    })


def checkoutSuccessHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    return render(request, 'checkout_success.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
    })


def ordersHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    confirmed_orders = []
    if request.user.is_authenticated:
        confirmed_orders = Cart.objects.filter(status__gte=1)

    return render(request, 'orders.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
        'confirmed_orders': confirmed_orders,
    })


def ordersItemHandler(request, order_id):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    order_items = []
    main_order = None
    if request.user.is_authenticated:
        order_items = CartItem.objects.filter(cart__id=order_id)
        main_order = Cart.objects.get(id=order_id)

    return render(request, 'order_item.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
        'order_items': order_items,
        'main_order': main_order,
    })


def compareHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    compare_list = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

        compare_list = CompareItem.objects.filter(session_id=user_session_id)

    return render(request, 'compare.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
        'compare_list': compare_list,
    })


def wishHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    wish_list = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

        wish_list = WishItem.objects.filter(session_id=user_session_id)

    return render(request, 'wish.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
        'wish_list': wish_list,
    })


def searchHandler(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    new_cart = None
    cart_items = []
    user_session_id = request.session.session_key

    if user_session_id:
        open_carts = Cart.objects.filter(session_id=user_session_id).filter(status=0)
        if open_carts:
            new_cart = open_carts[0]
            cart_items = CartItem.objects.filter(cart__id=new_cart.id).filter(status=0)

    search_items = []
    q = request.GET.get('q', None)
    if q:
        search_items = Product.objects.filter(title__contains=q)

    return render(request, 'search.html', {
        'categories': categories,
        'products': products,
        'new_cart': new_cart,
        'cart_items': cart_items,
        'search_items': search_items,
    })