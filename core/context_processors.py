from core.models import Product, ProductReview, ProductImages, CartOrder, Category, Address, Vendor, Wishlist, \
    CartOrderItems
from taggit.models import Tag
from django.db.models import Min, Max


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    tags = Tag.objects.all()
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))
    # min_price = min_max_price.get('price__min')
    # max_price = min_max_price.get('price__max')
    cart_total_amount = 0
    if 'cart' in request.session:
        for product_id, item in request.session['cart'].items():
            cart_total_amount += int(item['quantity']) * (float(item['price']))
    try:
        address = Address.objects.get(user=request.user, status=True)
    except:
        address = None
    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        wishlist = Wishlist.objects.filter(user__isnull=True)
    products = Product.objects.filter(product_status='published')
    deal_products = Product.objects.filter(product_status='published', featured=True)
    return {
        'categories': categories,
        'address': address,
        'vendors': vendors,
        'tags': tags,
        # 'min_price': min_price - 1,
        # 'max_price': max_price + 1,
        'min_max_price': min_max_price,
        'products': products,
        'cart_total_amount': float(cart_total_amount),
        'wishlist': wishlist,
        'deal_products': deal_products,
    }
