from django.contrib import admin
from core.models import Product, ProductReview, ProductImages, CartOrder, Category, Address, Vendor, Wishlist, \
    CartOrderItems


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['product_image', 'title', 'user', 'category', 'price', 'product_status', 'in_stock', 'featured']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'vendor_image']


@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']


@admin.register(CartOrderItems)
class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order_objects', 'invoice_no', 'item', 'order_image', 'quantity', 'price', 'total']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['review_status', 'user', 'parent', 'product', 'review', 'rating']

    @admin.display()
    def get_parent(self, obj):
        if obj.comment.parent:
            return obj.comment.parent
        return None


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_editable = ['status']
    list_display = ['user', 'address', 'status']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

# admin.site.register(Product, ProductAdmin)
# admin.site.register(Vendor, VendorAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(ProductReview, ProductImagesAdmin)
# admin.site.register(CartOrder, CartOrderAdmin)
# admin.site.register(CartOrderItems, CartOrderItemsAdmin)
# admin.site.register(Wishlist, WishlistAdmin)
# admin.site.register(Address, AddressAdmin)
