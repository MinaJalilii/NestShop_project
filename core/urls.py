from django.urls import path, include
from core.views import *

app_name = 'home'
urlpatterns = [
    # Home page
    path("", home_view, name='home'),

    # Products
    path("products", product_list_view, name='product-list'),
    path("product/<pid>", product_detail_view, name="product-detail"),

    # Categories
    path("categories", category_list_view, name='category-list'),
    path("<cid>/products", category_product_list_view, name='category_product_list'),

    # Vendors
    path("vendors", vendor_list_view, name='vendor-list'),
    path("vendor/<vid>", vendor_detail_view, name='vendor-detail'),

    # Tags
    path("tags/<slug:tag_slug>", tag_list, name='tag-list'),

    # Reviews,
    path("ajax_add_review/<int:pid>", ajax_add_review, name='ajax_add_review'),

    # Search
    path("search", search_view, name='search'),
    path("vendor-search", vendor_search_view, name="vendor-search"),

    # Filter Products
    path("filter-products", filter_product, name='filter-product'),

    # Add to cart
    path("add-to-cart", add_to_cart_view, name='add-to-cart'),

    # Cart page
    path("cart", cart_view, name='cart'),

    # Delete product from cart page
    path("delete-from-cart", delete_product_from_cart, name='delete-from-cart'),

    # Update quantity
    path("update-cart", update_cart, name='update-cart'),

    # Checkout page
    path("checkout", checkout, name='checkout'),

    # Paypal
    path("paypal/", include('paypal.standard.ipn.urls')),

    # Successful payment
    path("payment-success", paypal_success, name="payment-success"),

    # Failed payment
    path("payment-failed", paypal_fail, name="payment-failed"),

    # User dashboard
    path("dashboard", user_dashboard, name="dashboard"),

    # Order detail
    path("dashboard/order/<int:pk>", order_detail, name="order-detail"),

    # Make default address
    path("make-default-address", make_default_address, name="make-default-address"),

    # Empty cart
    path("empty-cart", empty_cart, name="empty-cart"),

    # Add to wishlist
    path("add-to-wishlist", add_to_wishlist, name="add-to-wishlist"),

    # View wishlist
    path("wishlist", wishlist_view, name="wishlist"),

    # Remove from wishlist
    path("remove-from-wishlist", remove_from_wishlist, name="remove-from-wishlist"),

    # About Us
    path("about-us", about_us_view, name="about-us"),

    # Blog List
    path("blogs", blog_list_view, name="blog-list"),
]
