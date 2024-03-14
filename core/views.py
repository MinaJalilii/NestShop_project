from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404, redirect
from django.template.loader import render_to_string
from core.models import Product, ProductReview, CartOrder, Category, Address, Vendor, Wishlist, \
    CartOrderItems
from userauths.models import Profile
from taggit.models import Tag
from django.db.models import Count, Avg
from core.forms import ProductReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import calendar


def home_view(request):
    products = Product.objects.filter(product_status='published')
    return render(request, 'core/index.html', {'products': products})


def product_list_view(request):
    products = Product.objects.filter(product_status='published')
    return render(request, 'core/product-list.html', {'products': products})


def category_list_view(request):
    categories = Category.objects.all()
    return render(request, 'core/category-list.html', {'categories': categories})


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)

    return render(request, 'core/category-product-list.html', {'category': category, 'products': products})


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    return render(request, 'core/vendors-list.html', {'vendors': vendors})


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status='published', vendor=vendor)
    categories = Category.objects.all()
    return render(request, 'core/vendor-details.html',
                  {'vendor': vendor, 'products': products, 'categories': categories})


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    product_images = product.images.all()
    related_products = Product.objects.filter(category=product.category).exclude(pid=pid)
    products = Product.objects.all().order_by('-date').exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    avg_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
    return render(request, 'core/product-detail.html',
                  {'product': product, 'product_images': product_images,
                   'related_products': related_products, 'products': products, 'reviews': reviews,
                   'avg_rating': avg_rating, 'review_form': review_form, 'make_review': make_review})


def tag_list(request, tag_slug):
    products = Product.objects.filter(product_status='published').order_by('-id')
    tag = get_list_or_404(Tag, slug=tag_slug)
    products = products.filter(tags__in=tag)
    return render(request, 'core/tag.html', {'tag': tag, 'products': products})


def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST.get('review'),
        rating=request.POST.get('rating'),
    )
    context = {
        'user': user.username,
        'review': request.POST.get('review'),
        'rating': request.POST.get('rating'),
    }
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    avg_reviews = avg_reviews.get('rating')
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'avg_reviews': avg_reviews,
        }
    )


def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query).order_by('-date')
    return render(request, 'core/search.html', {'products': products, 'query': query})


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    tags = request.GET.getlist('tag[]')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    products = Product.objects.filter(product_status='published').order_by('-date').distinct()
    products = products.filter(price__gte=min_price, price__lte=max_price)
    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    if len(tags) > 0:
        products = products.filter(tags__id__in=tags).distinct()

    data = render_to_string("core/async/product-list.html", {'products': products})

    return JsonResponse({'data': data})


def add_to_cart_view(request):
    cart_product = {}
    cart_product[str(request.GET.get('id'))] = {
        'title': request.GET.get('title'),
        'quantity': request.GET.get('quantity'),
        'price': request.GET.get('price'),
        'pid': request.GET.get('pid'),
        'image': request.GET.get('image'),
    }
    if 'cart' in request.session:
        if str(request.GET.get('id')) in request.session['cart']:
            cart_data = request.session['cart']
            cart_data[str(request.GET.get('id'))]['quantity'] = int(
                cart_product[str(request.GET.get('id'))]['quantity'])
            cart_data.update(cart_data)
            request.session['cart'] = cart_data
        else:
            cart_data = request.session['cart']
            cart_data.update(cart_product)
            request.session['cart'] = cart_data
    else:
        request.session['cart'] = cart_product
    context = render_to_string('core/async/cart-list.html', {'cart': request.session['cart']})
    cart_total_amount = 0
    for product_id, item in request.session['cart'].items():
        cart_total_amount += int(item['quantity']) * (float(item['price']))
    return JsonResponse({
        'data': request.session['cart'],
        'context': context,
        'total_items': len(request.session['cart']),
        'cart_total_amount': cart_total_amount,
    })


def cart_view(request):
    if 'cart' in request.session:
        return render(request, 'core/cart.html',
                      {'cart': request.session['cart'],
                       'total_items': len(request.session['cart'])})
    else:
        return render(request, 'core/cart.html', {})


def delete_product_from_cart(request):
    product_id = str(request.GET.get('id'))
    if 'cart' in request.session:
        if product_id in request.session['cart']:
            del request.session['cart'][product_id]
            request.session.modified = True
    cart_total_amount = 0
    for product_id, item in request.session['cart'].items():
        cart_total_amount += int(item['quantity']) * (float(item['price']))
    # context = render_to_string('core/async/cart-list.html', {'cart': request.session['cart'],
    #                                                          'total_items': len(request.session['cart']),
    #                                                          'cart_total_amount': cart_total_amount})
    return JsonResponse({
        # 'mydata': context,
        'total_items': len(request.session['cart']),
        'cart_total_amount': cart_total_amount
    })


def update_cart(request):
    product_id = str(request.GET.get('id'))
    product_quantity = request.GET.get('quantity')
    if 'cart' in request.session:
        if product_id in request.session['cart']:
            request.session['cart'][str(request.GET.get('id'))]['quantity'] = product_quantity
            request.session.modified = True
    cart_total_amount = 0
    for product_id, item in request.session['cart'].items():
        cart_total_amount += int(item['quantity']) * (float(item['price']))
    # context = render_to_string('core/async/cart-list.html', {'cart': request.session['cart']})
    return JsonResponse({
        # 'mydata': context,
        'total_items': len(request.session['cart']),
        'cart_total_amount': float(cart_total_amount),
        'product_quantity': product_quantity,
    })


@login_required
def checkout(request):
    if 'cart' in request.session:
        if len(request.session['cart']) > 0:
            return render(request, 'core/checkout.html',
                          {'cart': request.session['cart'],
                           'total_items': len(request.session['cart'])})
    else:
        messages.add_message(request, messages.INFO, 'Your cart is empty..')
        return redirect('home:product-list')


@login_required
def paypal_success(request):
    cart_total_amount = 0
    total_amount = 0
    if 'cart' in request.session:
        for product_id, item in request.session['cart'].items():
            total_amount += int(item['quantity']) * (float(item['price']))
        order = CartOrder.objects.create(user=request.user, price=total_amount)
        for product_id, item in request.session['cart'].items():
            cart_total_amount += int(item['quantity']) * (float(item['price']))
            cart_order_products = CartOrderItems.objects.create(
                order=order,
                invoice_no='INVOICE_NO-' + str(order.id),
                item=item['title'],
                image=item['image'],
                quantity=item['quantity'],
                price=item['price'],
                total=int(item['quantity']) * (float(item['price']))
            )
        # host = request.get_host()
        # paypal_dict = {
        #     'business': settings.PAYPAL_RECEIVER_EMAIL,
        #     'amount': cart_total_amount,
        #     'item_name': 'Order-Item-No-'+str(order.id),
        #     'invoice': 'INV_No-'+str(order.id),
        #     'currency_code': 'USD',
        #     'notify_url': 'https://{}{}'.format(host, reverse('home:paypal-ipn')),
        #     'return_url': 'https://{}{}'.format(host, reverse('home:payment-success')),
        #     'cancel_return': "https://{}{}".format(host, reverse('home:payment-failed')),
        # }
        # paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
        return render(request, 'core/paypal_success.html',
                      {'cart': request.session['cart'],
                       'total_items': len(request.session['cart'])})
    else:
        return render(request, 'core/paypal_success.html', {})


@login_required
def paypal_fail(request):
    pass


@login_required
def user_dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None
    orders = CartOrder.objects.filter(user=request.user)
    chart_orders = CartOrder.objects.filter(user=request.user).annotate(month=ExtractMonth('order_date')).values(
        'month').annotate(
        count=Count('id')).values('month', 'count')
    month = []
    total_orders = []
    for order in chart_orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])
    addresses = Address.objects.filter(user=request.user)
    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile
        )
        messages.success(request, 'Address added successfully.')
        return redirect('home:dashboard')
    context = {
        'orders': orders, 'addresses': addresses, 'profile': profile, 'chart_orders': chart_orders,
        'month': month, 'total_orders': total_orders,

    }
    return render(request, 'core/dashboard.html', context)


def order_detail(request, pk):
    order = CartOrder.objects.get(user=request.user, id=pk)
    order_items = CartOrderItems.objects.filter(order=order)
    return render(request, 'core/order_detail.html', {'order_items': order_items})


def make_default_address(request):
    address_id = request.GET.get('id')
    Address.objects.update(status=False)
    Address.objects.filter(id=address_id).update(status=True)

    return JsonResponse({
        'Boolean': True,
    })


def empty_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
        return redirect('home:home')
    else:
        return redirect('home:home')


def add_to_wishlist(request):
    product_id = request.GET.get('id')
    product = Product.objects.get(id=product_id)
    try:
        wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    except:
        wishlist_count = Wishlist.objects.filter(product=product, user__isnull=True).count()
    if wishlist_count > 0:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            wishlist = Wishlist.objects.filter(user__isnull=True)
        context = {
            'boolean': True,
            'wishlist': wishlist.count(),
        }
    else:
        try:
            Wishlist.objects.create(product=product, user=request.user)
        except:
            Wishlist.objects.create(product=product, user=None)
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            wishlist = Wishlist.objects.filter(user__isnull=True)
        context = {
            'boolean': True,
            'wishlist': wishlist.count(),
        }
    return JsonResponse(context)


def wishlist_view(request):
    try:
        wish_products = Wishlist.objects.filter(user=request.user)
    except:
        wish_products = Wishlist.objects.filter(user__isnull=True)
    return render(request, 'core/wishlist.html', {'wish_products': wish_products})


def remove_from_wishlist(request):
    product_id = request.GET.get('id')
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        wishlist = Wishlist.objects.filter(user__isnull=True)
    Wishlist.objects.get(id=product_id).delete()
    context = {
        'boolean': True,
        'wishlist': wishlist.count(),
    }
    return JsonResponse(context)


def about_us_view(request):
    return render(request, 'core/about.html', {})


def blog_list_view(request):
    return render(request, 'core/blogs.html', {})


def vendor_search_view(request):
    query = request.GET.get('vendor-q')
    vendors = Vendor.objects.filter(title__icontains=query).order_by('-date')
    return render(request, 'core/vendor-search.html', {'vendors': vendors, 'query': query})


def all_deals_view(request):
    return render(request, 'core/all-deals.html', {})


def compare_products_view(request):
    return render(request, 'core/products-compare.html', {})
