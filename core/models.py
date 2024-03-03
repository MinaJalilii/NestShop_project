from django.utils.safestring import mark_safe
from django.db import models
from userauths.models import User
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager

STATUS_CHOICE = (
    ('processing', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)

STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★')
)


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh123456', prefix='cat')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category')

    class Meta:
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % self.image.url)

    def __str__(self):
        return self.title


class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh123456', prefix='ven')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    cover_image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    chat_resp_time = models.CharField(max_length=100)
    shipping_on_time = models.CharField(max_length=100)
    authentic_rating = models.CharField(max_length=100)
    days_return = models.CharField(max_length=100)
    warranty_period = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % self.image.url)

    def __str__(self):
        return self.title


class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefgh123456', prefix='prd')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    old_price = models.DecimalField(max_digits=1000, decimal_places=2)
    specifications = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=100, default='Organic', null=True, blank=True)
    stock_count = models.CharField(max_length=100, default='10', null=True, blank=True)
    life = models.CharField(max_length=100, default='100 Days', null=True, blank=True)
    mfd = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    tags = TaggableManager()
    product_status = models.CharField(choices=STATUS, max_length=10)
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, alphabet='1234567890', prefix='sku')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    def product_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % self.image.url)

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.price * 100) / self.old_price
        return new_price


class ProductImages(models.Model):
    image = models.ImageField(upload_to='product-images')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='images')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Images'


# ------------------------Cart, Orders, OrderItems and Address---------------------------#
# ------------------------Cart, Orders, OrderItems and Address---------------------------#
# ------------------------Cart, Orders, OrderItems and Address---------------------------#
# ------------------------Cart, Orders, OrderItems and Address---------------------------#
# ------------------------Cart, Orders, OrderItems and Address---------------------------#

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    paid_status = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default='Processing')

    class Meta:
        verbose_name_plural = 'Cart Order'


class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=1000, decimal_places=2)
    total = models.DecimalField(max_digits=1000, decimal_places=2)

    def order_image(self):
        return mark_safe('<img src="%s" width="50"  height="50" />' % self.image)

    class Meta:
        verbose_name_plural = 'Cart Order Items'

    def order_objects(self):
        return f"Order_NO-{self.order.id}|user:{self.order.user.email}"


# ------------------------Product Review, Wishlists and Address---------------------------#
# ------------------------Product Review, Wishlists and Address---------------------------#
# ------------------------Product Review, Wishlists and Address---------------------------#
# ------------------------Product Review, Wishlists and Address---------------------------#
# ------------------------Product Review, Wishlists and Address---------------------------#


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review = models.TextField(null=True)
    rating = models.PositiveIntegerField(choices=RATING, default=None, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        return f"{self.user.username}: {self.user.email}"

    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='wishlist')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.CharField(max_length=11, null=True)
    address = models.CharField(max_length=200, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Address'
